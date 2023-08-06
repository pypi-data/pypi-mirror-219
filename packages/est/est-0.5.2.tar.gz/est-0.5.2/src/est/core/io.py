"""simple helper functions to insure a simple link with the `io` module (and XASObject)"""

import logging
from typing import Optional, Union
import h5py
from silx.io.url import DataUrl

from est.io import read_xas, write_xas
from est.core.types import XASObject
from est.core.types import dimensions as dimensions_mod
from est.units import ur
from est.io.utils.information import InputInformation
from est.io.utils import url as url_utils


_logger = logging.getLogger(__name__)

DEFAULT_SPECTRA_PATH = "/data/NXdata/data"

DEFAULT_CHANNEL_PATH = "/data/NXdata/Channel"

DEFAULT_CONF_PATH = "/configuration"


def read(
    spectra_url,
    channel_url,
    dimensions: Optional[dimensions_mod.DimensionsType] = None,
    config_url=None,
    energy_unit=ur.eV,
):
    """

    :param DataUrl spectra_url: data url to the spectra
    :param DataUrl channel_url: data url to the channel / energy
    :param DataUrl config_url: data url to the process configuration
    :param dimensions: way the data has been stored.
                       Usually is (X, Y, channels) of (Channels, Y, X).
                       If None, by default is considered to be (Z, Y, X)
    :type: tuple
    :return:
    :rtype: XASObject
    """
    reader = XASReader()
    return reader.read_frm_url(
        InputInformation(
            spectra_url=spectra_url,
            channel_url=channel_url,
            config_url=config_url,
            dimensions=dimensions,
            energy_unit=energy_unit,
        )
    )


def read_frm_file(
    file_path,
    energy_unit=ur.eV,
    dimensions: Optional[dimensions_mod.DimensionsType] = None,
    columns_names: Union[None, dict] = None,
):
    """

    :param str file_path: path to the file containing the spectra. Must ba a
                          .dat file that pymca can handle or a .h5py with
                          default path
    :param tuple dimensions: dimensions of the input data. For ASCII file can
                             be (X, Y) or (Y, X)
    :param Union[None,tuple] columns: name of the column to take for .dat...
                                      files.
    :return XasObject created from the input
    :rtype: XASObject
    """
    if file_path in (None, ""):
        return
    reader = XASReader()
    return reader.read_from_file(
        file_path=file_path,
        energy_unit=energy_unit,
        dimensions=dimensions,
        columns_names=columns_names,
    )


class XASReader:
    """Simple reader of a xas file"""

    @staticmethod
    def read_frm_url(input_information):
        sp, en, conf = read_xas(information=input_information)
        return XASObject(spectra=sp, energy=en, configuration=conf)

    @staticmethod
    def read_from_file(
        file_path,
        energy_unit=ur.eV,
        dimensions: Optional[dimensions_mod.DimensionsType] = None,
        columns_names=None,
    ):
        """

        :param str file_path:
        :return: `.XASObject`
        """
        # TODO: we should be able to avoid calling the creation of an InputInformation
        if file_path.endswith((".dat", ".csv")):
            return XASReader.read_frm_url(
                InputInformation(
                    spectra_url=url_utils.build_spec_data_url(
                        file_path=file_path,
                        col_name=columns_names["mu"],
                    ),
                    channel_url=url_utils.build_spec_data_url(
                        file_path=file_path, col_name=columns_names["energy"]
                    ),
                    energy_unit=energy_unit,
                    dimensions=dimensions,
                )
            )
        elif file_path.endswith(".xmu"):
            return XASReader.read_frm_url(
                InputInformation(
                    spectra_url=DataUrl(file_path=file_path, scheme="larch"),
                    channel_url=DataUrl(file_path=file_path, scheme="larch"),
                    energy_unit=energy_unit,
                    dimensions=dimensions,
                )
            )
        elif h5py.is_hdf5(file_path):
            return XASReader.read_frm_url(
                InputInformation(
                    spectra_url=DataUrl(
                        file_path=file_path,
                        scheme="silx",
                        data_path=DEFAULT_SPECTRA_PATH,
                    ),
                    channel_url=DataUrl(
                        file_path=file_path,
                        scheme="silx",
                        data_path=DEFAULT_CHANNEL_PATH,
                    ),
                    config_url=DataUrl(
                        file_path=file_path, scheme="silx", data_path="configuration"
                    ),
                    energy_unit=energy_unit,
                    dimensions=dimensions,
                )
            )
        else:
            raise ValueError(
                "file type {} not managed, unable to load".format(file_path)
            )

    __call__ = read_from_file


class XASWriter:
    """
    class to write the output file. In this case we need a class in order to
    setup the output file before
    """

    def __init__(self):
        self._output_file = None

    @property
    def output_file(self):
        return self._output_file

    @output_file.setter
    def output_file(self, file_):
        self._output_file = file_

    def set_properties(self, properties):
        if "_output_file_setting" in properties:
            self._output_file = properties["_output_file_setting"]

    def dump_xas(self, xas_obj):
        """
        write the XASObject into a hdf5 file.

        :param xas_obj: object to be stored
        :type: Union[:class:`.XASObject`,dict]
        """
        if isinstance(xas_obj, dict):
            _xas_obj = XASObject.from_dict(xas_obj)
        else:
            _xas_obj = xas_obj

        if not self._output_file:
            _logger.warning(
                "no output file defined, please give path to the output file"
            )
            self._output_file = input()

        _logger.info("dump xas obj to {}".format(self._output_file))

        # write raw data
        write_xas(
            h5_file=self._output_file,
            energy=_xas_obj.energy,
            mu=_xas_obj.absorbed_beam(),
            entry=_xas_obj.entry,
        )

    __call__ = dump_xas
