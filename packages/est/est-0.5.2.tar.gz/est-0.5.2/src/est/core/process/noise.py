from est.core.types import XASObject
from .process import Process
import scipy.signal
import logging
import numpy

_logger = logging.getLogger(__name__)


def process_noise_savgol(
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
    :param callbacks: callback to execute.
    :param output: list to store the result, needed for pool processing
    :type: multiprocessing.manager.list
    :param output_dict: key is input spectrum, value is index in the output
                        list.
    :type: dict
    :return: processed spectrum
    :rtype: tuple (configuration, spectrum)
    """
    _logger.debug(
        "start noise with Savitsky-Golay on spectrum (%s, %s)"
        % (spectrum.x, spectrum.y)
    )
    if "noise" in configuration:
        configuration = configuration["noise"]
    if "window_size" not in configuration:
        raise ValueError("`window_size` should be specify. Missing in configuration")
    else:
        window_size = configuration["window_size"]
    if "polynomial_order" not in configuration:
        raise ValueError(
            "`polynomial_order` should be specify. Missing in configuration"
        )
    else:
        polynomial_order = configuration["polynomial_order"]

    if spectrum.edge_step is None:
        raise ValueError(
            "edge_step is None. Unable to compute noise. (edge_step is determine in pre_edge. You must run it first)"
        )

    if spectrum.e0 is None:
        raise ValueError(
            "e0 is None. Unable to compute noise. (e0 is determine in pre_edge. You must run it first)"
        )

    # compute noise. This is always done over the full spectrum
    # get e_min and e_max. Those will be
    smooth_spectrum = scipy.signal.savgol_filter(
        spectrum.mu, window_size, polynomial_order
    )
    noise = numpy.absolute(spectrum.mu - smooth_spectrum)
    spectrum.noise_savgol = noise
    # compute e_min and e_max. those are provided relative to the edge
    e_min = configuration.get("e_min", None)
    e_max = configuration.get("e_max", None)

    if e_min is None:
        e_min = spectrum.energy.min()
    else:
        e_min += spectrum.e0
    if e_max is None:
        e_max = spectrum.energy.max()
    else:
        e_max += spectrum.e0

    spectrum.larch_dict["noise_e_min"] = e_min
    spectrum.larch_dict["noise_e_max"] = e_max
    mask = (spectrum.energy > e_min) & (spectrum.energy < (e_max))

    if mask.any():
        spectrum.raw_noise_savgol = numpy.mean(noise[mask])
        spectrum.norm_noise_savgol = spectrum.raw_noise_savgol / spectrum.edge_step
    else:
        # Uses nan's instead of raising an exception. Otherwise we have much more failing workflows online (either E0 is wrong or the scan has not progressed past Emin, which is after the edge so the plots are fine).
        spectrum.raw_noise_savgol = numpy.nan
        spectrum.norm_noise_savgol = numpy.nan

    if callbacks:
        for callback in callbacks:
            callback()


class NoiseProcess(
    Process,
    name="noise",
    input_names=["xas_obj"],
    optional_input_names=["window_size", "polynomial_order", "e_min", "e_max"],
    output_names=["xas_obj"],
):
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

        parameters = {
            "window_size": self.get_input_value("window_size", 5),
            "polynomial_order": self.get_input_value("polynomial_order", 2),
        }
        if not self.missing_inputs.e_min:
            parameters["e_min"] = self.inputs.e_min
        if not self.missing_inputs.e_max:
            parameters["e_max"] = self.inputs.e_max
        _xas_obj.configuration["noise"] = parameters

        self.progress = 0.0
        self._pool_process(xas_obj=_xas_obj)
        self.progress = 100.0
        self.outputs.xas_obj = _xas_obj

    def _pool_process(self, xas_obj):
        assert isinstance(xas_obj, XASObject)
        n_s = len(xas_obj.spectra.data.flat)
        for i_s, spectrum in enumerate(xas_obj.spectra):
            process_noise_savgol(
                spectrum=spectrum,
                configuration=xas_obj.configuration,
                callbacks=self.callbacks,
                overwrite=True,
            )
            self.progress = i_s / n_s * 100.0

    def definition(self):
        return "noise using Savitsky-Golay algorithm"

    @staticmethod
    def program_name():
        return "noise_savgol"
