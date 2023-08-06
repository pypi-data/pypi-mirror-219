import copy
import logging
from typing import Optional, Union

import pint
import numpy
from silx.io.url import DataUrl

import est.io
from est.io.utils import get_data
from est.units import ur
from est.settings import DEFAULT_READ_TIMEOUT
from est.core.types import dimensions as dimensions_mod
from .spectra import Spectra


try:
    import larch
except ImportError:
    larch = None

_logger = logging.getLogger(__name__)


class XASObject:
    """Base class of XAS

    :param spectra: absorbed beam as a list of :class:`.Spectrum` or a
                    numpy.ndarray. If is a numpy array, the axes should
                    have the `STANDARD_DIMENSIONS` order.
    :type: Union[numpy.ndarray, list]
    :param energy: beam energy
    :type: numpy.ndarray of one dimension
    :param dict configuration: configuration of the different process
    :param int dim1: first dimension of the spectra
    :param int dim2: second dimension of the spectra
    :param str name: name of the object. Will be used for the hdf5 entry
    :param spectra_url: path to the spectra data if any. Used when serializing
                        the XASObject. Won't read it from it.
    :type: Union[None,str]
    :param spectra_url_dims: dimensions of the stored spectra. WARNING:
                                   this is different of the spectra dimension
                                   which should be given in the
                                   `STANDARD_DIMENSIONS` order
    :type: Union[tuple,None]
    :param energy_url: path to the energy / channel  data if any. Used when
                       serializing the XASObject. Won't read it from it.
    :type: Union[None,str]
    """

    def __init__(
        self,
        spectra=None,
        energy=None,
        configuration: Union[dict, None] = None,
        dim1: Union[int, None] = None,
        dim2: Union[int, None] = None,
        name: str = "scan1",
        spectra_url: Union[DataUrl, None] = None,
        spectra_url_dims: Optional[dimensions_mod.DimensionsType] = None,
        energy_url: Union[DataUrl, None] = None,
        check_energy: bool = True,
    ):
        if isinstance(energy, numpy.ndarray) and not isinstance(
            energy, pint.quantity.Quantity
        ):
            # automatic energy unit guess. convert energy provided in keV to eV
            # works because EXAFS data are never longer than 2 keV and a low
            # energy XANES is never shorter than 3 eV. See issue 30
            if (energy.max() - energy.min()) < 3.0:
                energy = energy * ur.keV
            else:
                energy = energy * ur.eV

        if energy is not None:
            energy = energy.m_as(ur.eV)

        self.__channels = None
        self.__spectra = Spectra(energy=energy)
        self.__dim1 = None
        self.__dim2 = None
        self.__entry_name = name
        self.__spectra_url = spectra_url
        self.__spectra_url_dims = spectra_url_dims
        self.__energy_url = energy_url
        self.spectra = (energy, spectra, dim1, dim2)
        self.configuration = configuration

    def attach_3d_array(self, attr_name, attr_value):
        """
        Attach to each attribute the provided value

        :param attr_name:
        :param attr_value:
        :return:
        """
        if isinstance(attr_value, DataUrl):
            data = get_data(attr_value)
        else:
            data = attr_value
        if not isinstance(data, numpy.ndarray):
            raise TypeError(
                "`attr_value` should be an instance of DataUrl "
                "referencing a numpy array or a numpy array not "
                "{}".format(type(data))
            )
        if data.ndim > 2:
            for spectrum, d in zip(self.spectra.data.flat, data):
                setattr(spectrum, attr_name, d)
        else:
            for spectrum in self.spectra.data.flat:
                setattr(spectrum, attr_name, data)

    @property
    def entry(self) -> str:
        return self.__entry_name

    @property
    def spectra(self):
        return self.__spectra

    @property
    def spectra_url(self) -> Union[None, DataUrl]:
        """Url from where the spectra is available.
        Used for object serialization"""
        return self.__spectra_url

    @spectra_url.setter
    def spectra_url(self, url: DataUrl):
        self.__spectra_url = url

    @property
    def spectra_url_dims(self) -> tuple:
        """used to interpret the spectra_url if any"""
        return self.__spectra_url_dims

    @spectra_url_dims.setter
    def spectra_url_dims(self, dims: tuple):
        self.__spectra_url_dims = dims

    @property
    def energy_url(self) -> Union[DataUrl, None]:
        """Url from where the energy is available.
        Used for object serialization"""
        return self.__energy_url

    @energy_url.setter
    def energy_url(self, url: DataUrl):
        self.__energy_url = url

    @property
    def normalized_energy(self):
        if self.spectra is not None:
            return self.spectra.data.flat[0].normalized_energy

    # TODO: should no take such a tuple in parameter but the different parameter
    # energy, spectra, dim1, dim2
    @spectra.setter
    def spectra(self, energy_spectra: tuple):
        if isinstance(energy_spectra, Spectra):
            self.__spectra = energy_spectra
        elif energy_spectra is None:
            return
        else:
            if not len(energy_spectra) == 4:
                raise ValueError(
                    "4 elements expected: energy, spectra, dim1 and dim2. get {} instead".format(
                        len(energy_spectra)
                    )
                )
            energy, spectra, dim1, dim2 = energy_spectra
            self.__spectra = Spectra(energy=energy, spectra=spectra)
            if dim1 is not None and dim2 is not None:
                self.__spectra.reshape((dim1, dim2))

    def get_spectrum(self, dim1_idx: int, dim2_idx: int) -> spectra:
        """Util function to access the spectrum at dim1_idx, dim2_idx"""
        return self.spectra[dim1_idx, dim2_idx]

    @property
    def energy(self) -> numpy.ndarray:
        """energy as a numpy array in eV.
        :note: cannot be with unit because use directly by xraylarch and pymca
        """
        return self.spectra.energy

    @property
    def configuration(self) -> dict:
        return self.__configuration

    @configuration.setter
    def configuration(self, configuration: dict):
        assert configuration is None or isinstance(configuration, dict)
        self.__configuration = configuration or {}

    def to_dict(self) -> dict:
        """convert the XAS object to a dict

        By default made to simply import raw data.

        :param with_process_details: used to embed a list of spectrum with
                                     intermediary result instead of only raw mu.
                                     This is needed especially for the
                                     pushworkflow actors to keep a trace of the
                                     processes.
        :type: bool
        """

        res = {
            "configuration": self.configuration,
            "dim1": self.spectra.shape[0],
            "dim2": self.spectra.shape[1],
            "energy": self.spectra.energy,
            "spectra": [spectrum.to_dict() for spectrum in self.spectra],
        }
        return res

    def absorbed_beam(self) -> numpy.ndarray:
        return self.spectra.map_to(data_info="mu")

    def load_frm_dict(self, ddict: dict):
        """load XAS values from a dict"""
        if not isinstance(ddict, dict):
            raise TypeError(f"ddict is expected to be a dict. Not {type(ddict)}")
        # TODO: is this correct? Shouldn't this be `self.spectra_url_dims`?
        #       We don't have a test for this.
        dimensions = dimensions_mod.STANDARD_DIMENSIONS
        # default yay of storing data
        from est.io import load_data  # avoid cyclic import

        """The dict can be on the scheme of the to_dict function, containing
        the spectra and the configuration. Otherwise we consider it is simply
        the spectra"""
        if "configuration" in ddict:
            self.configuration = ddict["configuration"]
        if "spectra" in ddict:
            self.spectra = Spectra.frm_dict(ddict["spectra"], dimensions=dimensions)
        else:
            self.spectra = None
        if "energy" in ddict:
            energy = ddict["energy"]
            if isinstance(energy, str):
                energy_url = DataUrl(path=energy)
                energy = load_data(
                    data_url=energy_url, name="energy", dimensions=dimensions
                )
        else:
            energy = None
        if "dim1" in ddict:
            dim1 = ddict["dim1"]
        else:
            dim1 = None
        if "dim2" in ddict:
            dim2 = ddict["dim2"]
        else:
            dim2 = None

        self.spectra.reshape((dim1, dim2))
        return self

    @staticmethod
    def from_dict(ddict: dict):
        return XASObject().load_frm_dict(ddict=ddict)

    @staticmethod
    def from_file(
        h5_file,
        entry="scan1",
        spectra_path="data/absorbed_beam",
        energy_path="data/energy",
        configuration_path="configuration",
        dimensions=None,
        timeout=DEFAULT_READ_TIMEOUT,
    ):
        # load only mu and energy from the file
        spectra_url = DataUrl(
            file_path=h5_file, data_path="/".join((entry, spectra_path)), scheme="silx"
        )
        energy_url = DataUrl(
            file_path=h5_file, data_path="/".join((entry, energy_path)), scheme="silx"
        )
        if configuration_path is None:
            config_url = None
        else:
            config_url = DataUrl(
                file_path=h5_file,
                data_path="/".join((entry, configuration_path)),
                scheme="silx",
            )
        from est.io.utils.information import InputInformation

        sp, en, conf = est.io.read_xas(
            InputInformation(
                spectra_url=spectra_url,
                channel_url=energy_url,
                config_url=config_url,
                dimensions=dimensions,
            ),
            timeout=timeout,
        )
        return XASObject(spectra=sp, energy=en, configuration=conf)

    def dump(self, h5_file: str):
        """dump the XAS object to a file_path within the Nexus format"""
        from est.core.io import XASWriter  # avoid cyclic import

        writer = XASWriter()
        # dump raw data
        writer.output_file = h5_file
        writer.dump_xas(xas_obj=self)

    def deepcopy(self):
        return self.from_dict(self.to_dict())

    def copy(self):
        """ """
        # To have dedicated h5 file we have to create one new h5 file for
        # for each process. For now there is no way to do it differently
        res = copy.copy(self)
        return res

    def __eq__(self, other):
        if other is None:
            return False
        return (
            isinstance(other, XASObject)
            and (
                (self.energy is None and other.energy is None)
                or numpy.array_equal(self.energy, other.energy)
            )
            and self.configuration == other.configuration
            and self.spectra,
            other.spectra,
        )

    @property
    def n_spectrum(self) -> int:
        """return the number of spectra"""
        return len(self.spectra.data.flat)
