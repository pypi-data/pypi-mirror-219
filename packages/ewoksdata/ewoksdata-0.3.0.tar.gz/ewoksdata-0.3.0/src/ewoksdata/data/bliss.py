import sys
import logging
from numbers import Integral, Number
from typing import Iterator, List, Optional, Tuple, Sequence, Union

import numpy
import h5py
import hdf5plugin  # noqa F401
from numpy.typing import ArrayLike
from silx.io import h5py_utils
from silx.utils import retry as retrymod
from silx.io.utils import get_data as silx_get_data
from blissdata.h5api import dynamic_hdf5

try:
    import gevent.queue  # noqa F401 bliss MR 5369
    from blissdata.data.node import get_node
    from blissdata.data.events.lima import ImageNotSaved
except ImportError:
    get_node = None

from . import hdf5
from . import nexus
from . import url


logger = logging.getLogger(__name__)


def get_data(
    data: Union[str, ArrayLike, Number], **options
) -> Union[numpy.ndarray, Number]:
    if isinstance(data, str):
        data_url = url.as_dataurl(data)
        filename, h5path, idx = url.h5dataset_url_parse(data_url)
        if filename.endswith(".h5") or filename.endswith(".nx"):
            return _get_hdf5_data(filename, h5path, idx=idx, **options)
        if not data_url.scheme():
            if sys.platform == "win32":
                data_url = f"fabio:///{data}"
            else:
                data_url = f"fabio://{data}"
        return silx_get_data(data_url)
    elif isinstance(data, (Sequence, Number, numpy.ndarray)):
        return data
    else:
        raise TypeError(type(data))


def get_image(*args, **kwargs) -> numpy.ndarray:
    data = get_data(*args, **kwargs)
    return numpy.atleast_2d(numpy.squeeze(data))


@h5py_utils.retry()
def _get_hdf5_data(filename: str, h5path: str, idx=None, **options) -> numpy.ndarray:
    with hdf5.h5context(filename, h5path, **options) as dset:
        if _is_bliss_file(dset):
            if "end_time" not in nexus.get_nxentry(dset):
                raise retrymod.RetryError
        if idx is None:
            idx = tuple()
        return dset[idx]


def iter_bliss_scan_data(
    filename: str,
    scan_nr: Integral,
    lima_names: Optional[List[str]] = None,
    counter_names: Optional[List[str]] = None,
    subscan: Optional[Integral] = None,
    **options,
) -> Iterator[dict]:
    """Iterate over the data from one Bliss scan. The counters are assumed to have
    many data values as scan points.

    :param str filename: the Bliss dataset filename
    :param Integral filename: the scan number in the dataset
    :param list lima_names: names of lima detectors
    :param list counter_names: names of non-lima detectors (you need to provide at least one)
    :param Integral subscan: subscan number (for example "10.2" has `scan_nr=10` and `subscan=2`)
    :param Number retry_timeout: timeout when it cannot access the data for `retry_timeout` seconds
    :param Number retry_period: interval in seconds between data access retries
    :yields dict: data
    """
    if not subscan:
        subscan = 1
    if counter_names is None:
        counter_names = list()
    with dynamic_hdf5.File(filename, lima_names=lima_names, **options) as root:
        scan = root[f"{scan_nr}.{subscan}"]
        # assert _is_bliss_file(scan), "Not a Bliss dataset file"
        measurement = scan["measurement"]
        instrument = scan["instrument"]
        datasets = {name: measurement[name] for name in counter_names}
        for name in lima_names:
            datasets[name] = instrument[f"{name}/data"]
        names = list(datasets.keys())
        for values in zip(*datasets.values()):
            yield dict(zip(names, values))


def iter_bliss_data(
    filename: str,
    scan_nr: Integral,
    lima_names: List[str],
    counter_names: List[str],
    subscan: Optional[Integral] = None,
    start_index: Optional[Integral] = None,
    **options,
) -> Iterator[Tuple[int, dict]]:
    """Iterate over the data from one Bliss scan. The counters are assumed to have
    many data values as scan points.

    :param str filename: the Bliss dataset filename
    :param Integral filename: the scan number in the dataset
    :param list lima_names: names of lima detectors
    :param list counter_names: names of non-lima detectors (you need to provide at least one)
    :param Integral subscan: subscan number (for example "10.2" has `scan_nr=10` and `subscan=2`)
    :param Number retry_timeout: timeout when it cannot access the data for `retry_timeout` seconds
    :param Number retry_period: interval in seconds between data access retries
    :param Integral start_index: start iterating from this scan point index
    :yields tuple: scan index, data
    """
    if start_index is None:
        start_index = 0
    for index, data in enumerate(
        iter_bliss_scan_data(
            filename,
            scan_nr,
            lima_names=lima_names,
            counter_names=counter_names,
            subscan=subscan,
            **options,
        )
    ):
        if index >= start_index:
            yield index, data


def _is_bliss_file(h5item: Union[h5py.Dataset, h5py.Group]) -> bool:
    return h5item.file.attrs.get("creator", "").lower() == "bliss"


def last_lima_image(db_name: str) -> ArrayLike:
    """Get last lima image from memory"""
    node = _get_node(db_name, "lima")
    node.from_stream = True
    dataview = node.get(-1)
    try:
        image = dataview.get_last_live_image()
    except AttributeError:
        image = None
    if image is None or image.data is None:
        raise RuntimeError("Cannot get last image from lima")
    return image.data


def iter_bliss_scan_data_from_memory(
    db_name: str,
    lima_names: List[str],
    counter_names: List[str],
    retry_timeout: Optional[Number] = None,
    retry_period: Optional[Number] = None,
):
    scan_node = _get_node(
        db_name, "scan", retry_timeout=retry_timeout, retry_period=retry_period
    )
    indices = {name: 0 for name in lima_names + counter_names}
    buffers = {name: list() for name in lima_names + counter_names}
    lima_acq_nb = dict()
    for event_type, node, event_data in scan_node.walk_events():
        if node.type == "lima":
            name = node.db_name.split(":")[-2]
            if name not in lima_names:
                continue
            dataview = _get_lima_dataview(
                node,
                indices[name],
                retry_timeout=retry_timeout,
                retry_period=retry_period,
            )
            current_lima_acq_nb = dataview.status_event.status["lima_acq_nb"]
            first_lima_acq_nb = lima_acq_nb.setdefault(name, current_lima_acq_nb)
            if first_lima_acq_nb != current_lima_acq_nb:
                logger.warning("lima is already acquiring the next scan")
                continue
            try:
                data = list(dataview)
            except ImageNotSaved:
                logger.warning(
                    "cannot read lima data from file because images are not being saved"
                )
                continue
            except Exception as e:
                logger.warning("cannot read lima data (%s)", str(e))
                continue
            indices[name] += len(data)
            buffers[name].extend(data)
        elif node.type == "channel":
            name = node.db_name.split(":")[-1]
            if name not in counter_names:
                continue
            if event_data:
                data = event_data.data
            else:
                data = node.get_as_array(indices[name], -1)
            indices[name] += len(data)
            buffers[name].extend(data)
        nyield = min(len(v) for v in buffers.values())
        if nyield:
            for i in range(nyield):
                yield {name: values[i] for name, values in buffers.items()}
            buffers = {name: values[nyield:] for name, values in buffers.items()}
        if event_type == event_type.END_SCAN:
            break


@retrymod.retry()
def _get_node(db_name: str, node_type: str):
    if get_node is None:
        raise ModuleNotFoundError("No module named 'blissdata'")
    node = get_node(db_name)
    if node is None:
        raise retrymod.RetryError(f"Redis node {db_name} does not exist")
    if node.type != node_type:
        raise RuntimeError(f"Not a Redis {node_type} node")
    return node


@retrymod.retry()
def _get_lima_dataview(node, start_index: int):
    dataview = node.get(start_index, -1)
    try:
        if dataview.status_event.proxy is None:
            raise retrymod.RetryError("Lima proxy not known (yet)")
    except Exception:
        raise retrymod.RetryError("Lima proxy not known (yet)")
    return dataview
