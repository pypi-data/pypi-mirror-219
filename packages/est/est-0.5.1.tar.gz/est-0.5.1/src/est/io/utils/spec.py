from silx.io.spech5 import SpecFile
from est.units import ur
import functools
import numpy
import logging

_logger = logging.getLogger(__name__)


@functools.lru_cache(maxsize=2)
def read_spectrum(
    spec_file,
    energy_col_name=None,
    absorption_col_name=None,
    monitor_col_name=None,
    energy_unit=ur.eV,
    scan_header_S=None,
):
    """
    :note: the cache is sued because we call twice the same function for energy
           and absorption


    :param str spec_file: path to the spec file containing the spectra
                          definition
    :param str energy_col_index:
    :param str absorption_col_index:
    :param Union[str,None] monitor_col_name: name of the column to get monitor
    :param Union[str,None] scan_header_S: name of the scan to consider

    :return: (energy, mu)
    :rtype: tuple energy and list of absorption
    """
    spec_file = SpecFile(spec_file)
    energy = None
    mu = None
    if energy_col_name is None:
        _logger.warning("Spec energy column name not provided. Try 'Column 1'")
        energy_col_name = "Column 1"
    if absorption_col_name is None:
        _logger.warning("Spec absorption column name not provided. Try 'Column 2'")
        absorption_col_name = "Column 2"

    for i_data, scan in enumerate(spec_file):
        # if a scan header 'title' is provided
        if scan_header_S is not None and scan_header_S != scan.scan_header_dict["S"]:
            continue

        if (
            energy_col_name not in scan.labels
            and absorption_col_name not in scan.labels
        ):
            continue

        # get energy
        if energy_col_name is not None:
            energy = spec_file.data_column_by_name(
                scan_index=i_data, label=energy_col_name
            )
            if energy is not None:
                energy = (energy * energy_unit).m_as(ur.eV)

        # get absorption
        if absorption_col_name is not None:
            mu = spec_file.data_column_by_name(
                scan_index=i_data, label=absorption_col_name
            )

            if energy is not None:
                assert len(mu) == len(
                    energy
                ), "different number of elements between energy {} and absorption {}".format(
                    len(energy), len(mu)
                )

        # get monitor
        if monitor_col_name is not None:
            monitor = spec_file.data_column_by_name(
                scan_index=i_data, label=monitor_col_name
            )

            mu = mu / monitor
            if numpy.any(mu == numpy.inf) or numpy.any(mu == -numpy.inf):
                _logger.warning(
                    "found inf values after mu division by the monitor. Replace them by 0"
                )
                mu[mu == numpy.inf] = 0
                mu[mu == -numpy.inf] = 0

        return energy, numpy.asarray(mu)
    return energy, mu
