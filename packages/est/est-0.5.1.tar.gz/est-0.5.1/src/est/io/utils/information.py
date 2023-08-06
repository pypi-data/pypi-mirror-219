from typing import Optional
from silx.io.url import DataUrl
from est.units import as_energy_unit
from est.core.types import dimensions as dimensions_mod
from est.units import ur


class InputInformation:
    """
    Utils class to store input information
    """

    def __init__(
        self,
        spectra_url=None,
        channel_url=None,
        config_url=None,
        dimensions: Optional[dimensions_mod.DimensionsType] = None,
        energy_unit=ur.eV,
    ):
        # main information
        self.__spectra_url = None
        self.__channel_url = None
        self.__dimensions = None
        self.__energy_unit = None

        # "fancy information"
        self.__I0_url = None
        self.__I1_url = None
        self.__I2_url = None
        self.__mu_ref_url = None

        self.spectra_url = spectra_url
        self.channel_url = channel_url
        self.config_url = config_url
        self.dimensions = dimensions_mod.parse_dimensions(dimensions)
        self.energy_unit = energy_unit

    @property
    def spectra_url(self) -> Optional[DataUrl]:
        return self.__spectra_url

    @spectra_url.setter
    def spectra_url(self, url: Optional[DataUrl]):
        self.__spectra_url = url

    @property
    def channel_url(self) -> Optional[DataUrl]:
        return self.__channel_url

    @channel_url.setter
    def channel_url(self, url: Optional[DataUrl]):
        self.__channel_url = url

    @property
    def dimensions(self) -> tuple:
        return self.__dimensions

    @dimensions.setter
    def dimensions(self, dims: tuple):
        self.__dimensions = dims

    @property
    def energy_unit(self) -> Optional[DataUrl]:
        return self.__energy_unit

    @energy_unit.setter
    def energy_unit(self, unit: Optional[DataUrl]):
        self.__energy_unit = unit

    @property
    def I0_url(self) -> Optional[DataUrl]:
        return self.__I0_url

    @I0_url.setter
    def I0_url(self, url: Optional[DataUrl]):
        self.__I0_url = url

    @property
    def I1_url(self) -> Optional[DataUrl]:
        return self.__I1_url

    @I1_url.setter
    def I1_url(self, url: Optional[DataUrl]):
        self.__I1_url = url

    @property
    def I2_url(self) -> Optional[DataUrl]:
        return self.__I2_url

    @I2_url.setter
    def I2_url(self, url: Optional[DataUrl]):
        self.__I2_url = url

    @property
    def mu_ref_url(self) -> Optional[DataUrl]:
        return self.__mu_ref_url

    @mu_ref_url.setter
    def mu_ref_url(self, url: Optional[DataUrl]):
        self.__mu_ref_url = url

    @property
    def scan_title_url(self) -> Optional[DataUrl]:
        return self._scan_title_url

    @scan_title_url.setter
    def scan_title_url(self, url: Optional[DataUrl]):
        self._scan_title_url = url

    def to_dict(self) -> dict:
        def dump_url(url):
            if url in (None, ""):
                return None
            else:
                return url.path()

        return {
            "spectra_url": dump_url(self.spectra_url),
            "channel_url": dump_url(self.channel_url),
            "config_url": dump_url(self.config_url),
            "dimensions": self.dimensions,
            "energy_unit": str(self.energy_unit),
            "I0_url": dump_url(self.I0_url),
            "I1_url": dump_url(self.I1_url),
            "I2_url": dump_url(self.I2_url),
            "mu_ref_url": dump_url(self.mu_ref_url),
        }

    @staticmethod
    def from_dict(ddict: dict):
        spectra_url = ddict.get("spectra_url", None)
        channel_url = ddict.get("channel_url", None)
        dimensions = ddict.get("dimensions", None)
        config_url = ddict.get("config_url", None)
        energy_unit = ddict.get("energy_unit", None)

        def load_url(url):
            if url in (None, ""):
                return None
            else:
                return DataUrl(path=url)

        info = InputInformation(
            spectra_url=load_url(spectra_url),
            channel_url=load_url(channel_url),
            dimensions=dimensions,
            config_url=load_url(config_url),
            energy_unit=as_energy_unit(energy_unit),
        )

        I0_url = ddict.get("I0_url", None)
        I1_url = ddict.get("I1_url", None)
        I2_url = ddict.get("I2_url", None)
        mu_ref_url = ddict.get("mu_ref_url", None)
        info.I0_url = I0_url
        info.I1_url = I1_url
        info.I2_url = I2_url
        info.mu_ref_url = mu_ref_url

        return info
