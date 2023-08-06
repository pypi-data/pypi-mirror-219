import logging
import h5py
from silx.io.dictdump import h5todict
import silx.io.h5py_utils
import silx.io.utils
from est import settings


_logger = logging.getLogger(__name__)


@silx.io.h5py_utils.retry(retry_timeout=settings.DEFAULT_READ_TIMEOUT)
def get_data(url):
    """Returns a numpy data from an URL.

    Examples:

    >>> # 1st frame from an EDF using silx.io.open
    >>> data = silx.io.get_data("silx:/users/foo/image.edf::/scan_0/instrument/detector_0/data[0]")

    >>> # 1st frame from an EDF using fabio
    >>> data = silx.io.get_data("fabio:/users/foo/image.edf::[0]")

    Yet 2 schemes are supported by the function.

    - If `silx` scheme is used, the file is opened using
        :meth:`silx.io.open`
        and the data is reach using usually NeXus paths.
    - If `fabio` scheme is used, the file is opened using :meth:`fabio.open`
        from the FabIO library.
        No data path have to be specified, but each frames can be accessed
        using the data slicing.
        This shortcut of :meth:`silx.io.open` allow to have a faster access to
        the data.

    .. seealso:: :class:`silx.io.url.DataUrl`

    :param Union[str,silx.io.url.DataUrl]: A data URL
    :rtype: Union[numpy.ndarray, numpy.generic]
    :raises ImportError: If the mandatory library to read the file is not
        available.
    :raises ValueError: If the URL is not valid or do not match the data
    :raises IOError: If the file is not found or in case of internal error of
        :meth:`fabio.open` or :meth:`silx.io.open`. In this last case more
        informations are displayed in debug mode.
    """
    if not isinstance(url, silx.io.url.DataUrl):
        url = silx.io.url.DataUrl(url)

    if not url.is_valid():
        raise ValueError("URL '%s' is not valid" % url.path())

    if url.scheme() == "silx":
        data_path = url.data_path()
        data_slice = url.data_slice()

        with silx.io.h5py_utils.File(url.file_path(), "r") as h5:
            dset = h5[data_path]

            if not silx.io.is_dataset(dset):
                raise ValueError(
                    "Data path from URL '%s' is not a dataset" % url.path()
                )

            if data_slice is not None:
                data = silx.io.utils.h5py_read_dataset(dset, index=data_slice)
            else:
                # works for scalar and array
                data = silx.io.utils.h5py_read_dataset(dset)

    elif url.scheme() == "fabio":
        import fabio

        data_slice = url.data_slice()
        if data_slice is None:
            data_slice = (0,)
        if data_slice is None or len(data_slice) != 1:
            raise ValueError(
                "Fabio slice expect a single frame, but %s found" % data_slice
            )
        index = data_slice[0]
        if not isinstance(index, int):
            raise ValueError(
                "Fabio slice expect a single integer, but %s found" % data_slice
            )

        try:
            fabio_file = fabio.open(url.file_path())
        except Exception:
            raise IOError(
                "Error while opening %s with fabio (use debug for more information)"
                % url.path()
            )

        if fabio_file.nframes == 1:
            if index != 0:
                raise ValueError(
                    "Only a single frame available. Slice %s out of range" % index
                )
            data = fabio_file.data
        else:
            data = fabio_file.getframe(index).data

        # There is no explicit close
        fabio_file = None

    else:
        raise ValueError("Scheme '%s' not supported" % url.scheme())

    return data


@silx.io.h5py_utils.retry(retry_timeout=settings.DEFAULT_READ_TIMEOUT)
def get_est_data(url):
    spectra = []
    with silx.io.h5py_utils.File(url.file_path(), "r") as hdf5:
        # get all possible entries
        entries = filter(
            lambda x: isinstance(hdf5[x], h5py.Group)
            and "est_saving_pt" in hdf5[x].keys(),
            hdf5.keys(),
        )
        entries = list(entries)
        if len(entries) == 0:
            _logger.error("no spectra dataset found in the file", url.file_path())
            return

        if len(entries) > 1:
            _logger.warning(
                "several entry detected, only one will be loaded:", entries[0]
            )
        spectra_path = "/".join((entries[0], "est_saving_pt", "spectra"))
        node_spectra = hdf5[spectra_path]
        spectrum_indexes = list(node_spectra.keys())
        spectrum_indexes = list(map(lambda x: int(x), spectrum_indexes))
        spectrum_indexes.sort()
    from est.core.types import Spectrum

    for index in spectrum_indexes:
        spectrum_path = "/".join((spectra_path, str(index)))
        dict_ = h5todict(h5file=url.file_path(), path=spectrum_path, asarray=False)
        spectrum = Spectrum.from_dict(dict_)
        spectra.append(spectrum)
    return spectra
