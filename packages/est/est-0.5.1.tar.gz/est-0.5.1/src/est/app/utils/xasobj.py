import logging
from silx.io.url import DataUrl

from est import settings
from est.io.utils import get_data
from est.core.types import XASObject
from est.core.io import read_xas
from est.io.utils.information import InputInformation


_logger = logging.getLogger(__name__)


def get_xas_obj(
    input_information: InputInformation, timeout=settings.DEFAULT_READ_TIMEOUT
):
    """load xas object from command line input
    :param spec_input: tuple of Union[str, None, dict]
    :param float timeout: read time out (for hdf5 only for now)
    """
    sp, en, conf = read_xas(information=input_information, timeout=timeout)
    xas_obj = XASObject(spectra=sp, energy=en, configuration=conf)
    attr_names = "I0", "I1", "I2", "mu_ref"
    attr_values = (
        getattr(input_information, "I0", None),
        getattr(input_information, "I1", None),
        getattr(input_information, "I2", None),
        getattr(input_information, "mu_ref", None),
    )
    for attr_name, attr_value in zip(attr_names, attr_values):
        if attr_value is not None:
            if isinstance(attr_value, DataUrl):
                data = get_data(attr_value)
            else:
                data = attr_value
            if data.shape[0] > xas_obj.energy.shape[0]:
                _logger.warning(
                    "energy has less value than dataset. Clip {}.".format(attr_name)
                )
                data = data[: xas_obj.energy.shape[0]]
            xas_obj.attach_3d_array(attr_name, data)
    return xas_obj
