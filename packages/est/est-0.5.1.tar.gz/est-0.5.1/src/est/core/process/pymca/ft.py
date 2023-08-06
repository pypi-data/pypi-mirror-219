"""wrapper to pymca `ft` process"""

import logging
import numpy
from PyMca5.PyMcaPhysics.xas.XASClass import XASClass
from est.core.process.process import Process
from est.core.types import XASObject, Spectrum

_logger = logging.getLogger(__name__)


def process_spectr_ft(
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
        "start fourier transform on spectrum (%s, %s)" % (spectrum.x, spectrum.y)
    )
    pymca_xas = XASClass()
    if spectrum.energy is None or spectrum.mu is None:
        _logger.error(
            "Energy and or Mu is/are not specified, unable to " "compute exafs"
        )
        return None, None

    if configuration is not None:
        pymca_xas.setConfiguration(configuration)
    pymca_xas.setSpectrum(energy=spectrum.energy, mu=spectrum.mu)

    if spectrum.chi is None:
        _logger.warning(
            "exafs has not been processed yet, unable to process" "fourier transform"
        )
        return None, None

    if "EXAFSNormalized" not in spectrum.pymca_dict:
        _logger.warning("ft window need to be defined first")
        return None, None

    cleanMu = spectrum.chi
    kValues = spectrum.k

    dataSet = numpy.zeros((cleanMu.size, 2), float)
    dataSet[:, 0] = kValues
    dataSet[:, 1] = cleanMu

    set2 = dataSet.copy()
    set2[:, 1] = spectrum.pymca_dict["EXAFSNormalized"]

    k_min = spectrum.pymca_dict.get("KMin", spectrum.k.max())
    k_max = spectrum.pymca_dict.get("KMax", spectrum.k.min())

    # remove points with k<2
    goodi = (set2[:, 0] >= k_min) & (set2[:, 0] <= k_max)
    set2 = set2[goodi, :]

    if set2.size == 0:
        ft = {"FTImaginary": numpy.nan, "FTIntensity": numpy.nan, "FTRadius": numpy.nan}
    else:
        ft = pymca_xas.fourierTransform(
            set2[:, 0],
            set2[:, 1],
            kMin=spectrum.pymca_dict["KMin"],
            kMax=spectrum.pymca_dict["KMax"],
        )
        assert "FTIntensity" in ft
        assert "FTRadius" in ft
        assert ft["FTRadius"] is not None
        assert ft["FTIntensity"] is not None
    if callbacks:
        for callback in callbacks:
            callback()

    if not overwrite:
        spectrum = Spectrum.from_dict(spectrum.to_dict())

    spectrum.ft = ft

    if output is not None:
        assert output_dict is not None
        output[output_dict[spectrum]] = spectrum
    return configuration, spectrum


def pymca_ft(xas_obj, **optional_inputs):
    """

    :param xas_obj: object containing the configuration and spectra to process
    :type: Union[XASObject, dict]
    :return: spectra dict
    :rtype: dict
    """
    process = PyMca_ft(inputs={"xas_obj": xas_obj, **optional_inputs})
    process.run()
    return process.get_output_value("xas_obj", None)


class PyMca_ft(
    Process,
    name="ft",
    input_names=["xas_obj"],
    output_names=["xas_obj"],
    optional_input_names=["ft"],
):
    def set_properties(self, properties):
        if "_pymcaSettings" in properties:
            self._settings = properties["_pymcaSettings"]

    def run(self):
        """

        :param xas_obj: object containing the configuration and spectra to process
        :type: Union[XASObject, dict]
        :return: spectra dict
        :rtype: dict
        """
        xas_obj = self.inputs.xas_obj
        if xas_obj is None:
            raise ValueError("xas_obj should be provided")
        _xas_obj = self.getXasObject(xas_obj=xas_obj)

        if self.inputs.ft:
            self.setConfiguration(self.inputs.ft)
            _xas_obj.configuration["FT"] = self.inputs.ft

        self._advancement.reset(max_=_xas_obj.n_spectrum)
        self._advancement.startProcess()
        self._pool_process(xas_obj=_xas_obj)
        self._advancement.endProcess()
        assert hasattr(_xas_obj.spectra.data.flat[0], "ft")
        assert hasattr(_xas_obj.spectra.data.flat[0].ft, "intensity")
        assert hasattr(_xas_obj.spectra.data.flat[0].ft, "imaginary")
        self.outputs.xas_obj = _xas_obj

    def _pool_process(self, xas_obj):
        assert isinstance(xas_obj, XASObject)
        n_s = len(xas_obj.spectra.data.flat)
        for i_s, spectrum in enumerate(xas_obj.spectra):
            process_spectr_ft(
                spectrum=spectrum,
                configuration=xas_obj.configuration,
                callbacks=self.callbacks,
                overwrite=True,
            )
            self.progress = i_s / n_s * 100.0

    def definition(self):
        return "fourier transform"

    def program_version(self):
        import PyMca5

        return PyMca5.version()

    @staticmethod
    def program_name():
        return "pymca_ft"
