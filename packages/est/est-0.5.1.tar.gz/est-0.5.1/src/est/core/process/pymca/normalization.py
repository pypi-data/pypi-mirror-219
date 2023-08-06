"""wrapper to pymca `normalization` process"""

import logging
from PyMca5.PyMcaPhysics.xas.XASClass import XASClass
from est.core.process.process import Process
from est.core.types import Spectrum, XASObject

_logger = logging.getLogger(__name__)


def process_spectr_norm(
    spectrum: Spectrum,
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
    :param callbacks: callback to execute.
    :param output: list to store the result, needed for pool processing
    :type: multiprocessing.manager.list
    :param output_dict: key is input spectrum, value is index in the output
                        list.
    :type: dict
    :return: processed spectrum
    :rtype: tuple (configuration, spectrum)
    """
    assert isinstance(spectrum, Spectrum)
    _logger.debug("start normalization on spectrum (%s, %s)" % (spectrum.x, spectrum.y))
    if spectrum.energy is None or spectrum.mu is None:
        _logger.error(
            "Energy and or Mu is/are not specified, unable to " "compute exafs"
        )
        return None, None
    pymca_xas = XASClass()
    pymca_xas.setSpectrum(energy=spectrum.energy, mu=spectrum.mu)
    if configuration is not None:
        if "e0" in configuration:
            configuration["E0Value"] = configuration["e0"]
            configuration["E0Method"] = "Manual"
        pymca_xas.setConfiguration(configuration)
    configuration = pymca_xas.getConfiguration()
    res = pymca_xas.normalize()

    if not overwrite:
        spectrum = Spectrum.from_dict(spectrum.to_dict())

    # set output we want to keep
    spectrum.normalized_energy = res.get("NormalizedEnergy", None)
    spectrum.normalized_mu = res.get("NormalizedMu", None)
    spectrum.e0 = res.get("Edge", None)
    spectrum.pre_edge = res.get("NormalizedBackground", None)
    spectrum.post_edge = res.get("NormalizedSignal", None)

    if callbacks:
        for callback in callbacks:
            callback()

    if output is not None:
        assert output_dict is not None
        output[output_dict[spectrum]] = spectrum

    return configuration, spectrum


def pymca_normalization(xas_obj, **optional_inputs):
    """

    :param xas_obj: object containing the configuration and spectra to process
    :type: Union[XASObject, dict]. If is a dict, should contain configuration or
                                 spectra keys. Otherwise is simply the spectra
    :return: spectra dict
    :rtype: dict
    """
    process = PyMca_normalization(inputs={"xas_obj": xas_obj, **optional_inputs})
    process.run()
    return process.get_output_value("xas_obj", None)


class PyMca_normalization(
    Process,
    name="normalization",
    input_names=["xas_obj"],
    output_names=["xas_obj"],
    optional_input_names=["normalization"],
):
    def set_properties(self, properties):
        if "_pymcaSettings" in properties:
            self._settings = properties["_pymcaSettings"]

    def run(self):
        """

        :param xas_obj: object containing the configuration and spectra to process
        :type: Union[XASObject, dict]. If is a dict, should contain configuration or
                                     spectra keys. Otherwise is simply the spectra
        :return: updated XASObject
        :rtype: :class:`.XASObject`
        """
        xas_obj = self.inputs.xas_obj
        if xas_obj is None:
            raise ValueError("xas_obj should be provided")
        xas_obj = self.getXasObject(xas_obj)

        if xas_obj.energy is None:
            _logger.error("Energy not specified, unable to normalize spectra")
            return

        if self.inputs.normalization:
            self.setConfiguration(self.inputs.normalization)
            xas_obj.configuration["Normalization"] = self.inputs.normalization
        self.progress = 0.0
        self._pool_process(xas_obj=xas_obj)
        self.progress = 100.0
        if xas_obj.normalized_energy is None:
            raise ValueError("Fail to compute normalize energy")

        self.outputs.xas_obj = xas_obj

    def _pool_process(self, xas_obj):
        """process normalization from a pool"""
        assert isinstance(xas_obj, XASObject)
        n_s = len(xas_obj.spectra.data.flat)
        for i_s, spectrum in enumerate(xas_obj.spectra.data.flat):
            process_spectr_norm(
                spectrum=spectrum,
                configuration=xas_obj.configuration,
                callbacks=self.callbacks,
                overwrite=True,
            )
            self.progress = i_s / n_s * 100.0

    def definition(self):
        return "Normalization of the spectrum"

    def program_version(self):
        import PyMca5

        return PyMca5.version()

    @staticmethod
    def program_name():
        return "pymca_normalization"
