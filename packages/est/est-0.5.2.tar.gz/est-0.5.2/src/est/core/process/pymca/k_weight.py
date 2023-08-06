"""wrapper to pymca `k-weight` process"""

import logging
from PyMca5.PyMcaPhysics.xas.XASClass import XASClass, e2k
from est.core.process.process import Process
from est.core.process.pymca.exafs import process_spectr_exafs
from est.core.types import XASObject, Spectrum

_logger = logging.getLogger(__name__)


def process_spectr_k(
    spectrum,
    configuration,
    overwrite=True,
    callbacks=None,
    output=None,
    output_dict=None,
):
    """

    :param spectrum: spectrum to process
    :type: :class:`.Spectrum`
    :param configuration: configuration of the pymca normalization
    :type: dict
    :param overwrite: False if we want to return a new Spectrum instance
    :type: bool
    :param callback: callback to execute.
    :param output: list to store the result, needed for pool processing
    :type: multiprocessing.manager.list
    :param output_dict: key is input spectrum, value is index in the output
                        list.
    :type: dict
    :return: processed spectrum
    :rtype: tuple (configuration, spectrum)
    """
    _logger.debug(
        "start k weight definition on spectrum (%s, %s)" % (spectrum.x, spectrum.y)
    )
    assert spectrum is not None

    pymca_xas = XASClass()
    if spectrum.energy is None or spectrum.mu is None:
        raise ValueError(
            "Energy and or Mu is/are not specified, unable to " "compute exafs"
        )
    pymca_xas.setSpectrum(energy=spectrum.energy, mu=spectrum.mu)
    if configuration is not None:
        if "KWeight" in configuration and configuration["KWeight"] is not None:
            configuration["FT"]["KWeight"] = configuration["KWeight"]
            configuration["EXAFS"]["KWeight"] = configuration["KWeight"]
        pymca_xas.setConfiguration(configuration)

    if not overwrite:
        spectrum = Spectrum.from_dict(spectrum.to_dict())

    # we need to update EXAFSNormalized since we are overwriting it
    cf, exafs_res = process_spectr_exafs(spectrum=spectrum, configuration=configuration)
    if exafs_res is None:
        err = "Failed to process exafs."
        if spectrum.x is not None or spectrum.y is not None:
            err = (
                err
                + "Spectrum (x, y) coords: "
                + ",".join((str(spectrum.x), str(spectrum.y)))
            )
        raise ValueError(err)

    # update EXAFSNormalized
    e0 = pymca_xas.calculateE0()

    kValues = e2k(spectrum.energy - e0)
    exafs = exafs_res.pymca_dict["EXAFSNormalized"]
    if "KWeight" in configuration and configuration["KWeight"] is not None:
        exafs *= pow(kValues, configuration["KWeight"])
        spectrum.pymca_dict["KWeight"] = configuration["KWeight"]

    spectrum.pymca_dict["EXAFSNormalized"] = exafs
    configuration_ = pymca_xas.getConfiguration()

    if callbacks:
        for callback in callbacks:
            callback()

    if output is not None:
        assert output_dict is not None
        output[output_dict[spectrum]] = spectrum
    return configuration_, spectrum


def pymca_k_weight(xas_obj, **optional_inputs):
    """
    Set weight for exafs values

    :param xas_obj: object containing the configuration and spectra to process
    :type: Union[:class:`.XASObject`, dict]
    :return: spectra dict
    :rtype: :class:`.XASObject`
    """
    process = PyMca_k_weight(inputs={"xas_obj": xas_obj, **optional_inputs})
    process.run()
    return process.get_output_value("xas_obj", None)


class PyMca_k_weight(
    Process,
    name="k weight",
    input_names=["xas_obj"],
    output_names=["xas_obj"],
    optional_input_names=["k_weight"],
):
    def set_properties(self, properties):
        if "_kWeightSetting" in properties:
            _properties = properties.copy()
            _properties["k_weight"] = _properties["_kWeightSetting"]
            del _properties["_kWeightSetting"]
            self.setConfiguration(_properties)

    def run(self):
        """

        :param xas_obj: object containing the configuration and spectra to process
        :type: Union[:class:`.XASObject`, dict]
        :return: spectra dict
        :rtype: :class:`.XASObject`
        """
        xas_obj = self.inputs.xas_obj
        if xas_obj is None:
            raise ValueError("xas_obj should be provided")
        _xas_obj = self.getXasObject(xas_obj=xas_obj)

        if self.inputs.k_weight:
            self.setConfiguration({"k_weight": self.inputs.k_weight})
            _xas_obj.configuration["SET_KWEIGHT"] = self.inputs.k_weight

        if "SET_KWEIGHT" not in _xas_obj.configuration:
            _logger.warning(
                "Missing configuration to know which value we should set "
                "to k weight, will be set to 0 by default"
            )
            _xas_obj.configuration["SET_KWEIGHT"] = 0

        for key in ("FT", "EXAFS", "Normalization"):
            if key not in _xas_obj.configuration:
                _xas_obj.configuration[key] = {}

        _xas_obj.configuration["KWeight"] = _xas_obj.configuration["SET_KWEIGHT"]
        _xas_obj.configuration["FT"]["KWeight"] = _xas_obj.configuration["SET_KWEIGHT"]
        _xas_obj.configuration["EXAFS"]["KWeight"] = _xas_obj.configuration[
            "SET_KWEIGHT"
        ]
        _xas_obj.configuration["Normalization"]["KWeight"] = _xas_obj.configuration[
            "SET_KWEIGHT"
        ]

        self._advancement.reset(max_=_xas_obj.n_spectrum)
        self.progress = 0.0
        self._pool_process(xas_obj=_xas_obj)
        self.progress = 100.0
        self.outputs.xas_obj = _xas_obj

    def _pool_process(self, xas_obj):
        """process normalization from a pool"""
        assert isinstance(xas_obj, XASObject)
        assert "KWeight" in xas_obj.configuration
        n_s = len(xas_obj.spectra.data.flat)
        for i_s, spectrum in enumerate(xas_obj.spectra.data.flat):
            process_spectr_k(
                spectrum=spectrum,
                configuration=xas_obj.configuration,
                callbacks=self.callbacks,
                overwrite=True,
            )
            assert "KWeight" in xas_obj.configuration
            self.progress = i_s / n_s * 100.0

    def definition(self):
        return "Define k weight for xas treatment"

    def program_version(self):
        import PyMca5

        return PyMca5.version()

    @staticmethod
    def program_name():
        return "pymca_k_weight"
