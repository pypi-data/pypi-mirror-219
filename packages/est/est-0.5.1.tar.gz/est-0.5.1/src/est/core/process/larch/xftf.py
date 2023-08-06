"""wrapper to the larch xftf process"""

from est.core.types import Spectrum, XASObject
from est.core.process.process import Process
from larch.xafs.xafsft import xftf
from larch.symboltable import Group
import logging

_logger = logging.getLogger(__name__)


def process_spectr_xftf(
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
    _logger.debug("start xftf on spectrum (%s, %s)" % (spectrum.x, spectrum.y))
    assert isinstance(spectrum, Spectrum)
    if spectrum.k is None or spectrum.chi is None:
        _logger.error(
            "k and/or chi is/are not specified, unable to compute "
            "xftf. Maybe you need to run autobk process before ?"
        )
        return None, None

    # if kmax is not provided take default value
    kmax = configuration.get("kmax", None)
    if kmax is None:
        configuration["kmax"] = max(spectrum.k) * 0.9
    kmin = configuration.get("kmin", None)
    if kmin is None:
        configuration["kmin"] = min(spectrum.k)

    opts = {}
    for opt_name in (
        "kmin",
        "kmax",
        "kweight",
        "dk",
        "dk2",
        "with_phase",
        "window",
        "rmax_out",
        "nfft",
        "kstep",
    ):
        if opt_name in configuration:
            opts[opt_name] = configuration[opt_name]
            if opt_name == "kweight":
                opts["kw"] = configuration[opt_name]
    if not overwrite:
        spectrum = Spectrum.from_dict(spectrum.to_dict())

    res_group = Group()
    xftf(k=spectrum.k, chi=spectrum.chi, group=res_group, **opts)
    spectrum.r = res_group.r
    spectrum.chir = res_group.chir
    spectrum.chir_mag = res_group.chir_mag
    spectrum.chir_re = res_group.chir_re
    spectrum.chir_im = res_group.chir_im
    with_phase = opts.get("with_phase", False)
    if with_phase:
        spectrum.chir_pha = res_group.chir_pha
    else:
        spectrum.chir_pha = None

    # handle chi(x) * k**k_weight plot with r max
    if spectrum.k is not None and spectrum.chi is not None:
        if "kweight" in opts:
            kweight = opts["kweight"]
        else:
            kweight = 0

    spectrum.chi_weighted_k = spectrum.chi * (spectrum.k**kweight)
    spectrum.larch_dict["xftf_k_weight"] = kweight
    spectrum.larch_dict["xftf_k_min"] = configuration["kmin"]
    spectrum.larch_dict["xftf_k_max"] = configuration["kmax"]

    if callbacks:
        for callback in callbacks:
            callback()

    return configuration, spectrum


def larch_xftf(xas_obj, **optional_inputs):
    """

    :param xas_obj: object containing the configuration and spectra to process
    :type: Union[XASObject, dict]
    :return: spectra dict
    :rtype: XASObject
    """
    process = Larch_xftf(inputs={"xas_obj": xas_obj, **optional_inputs})
    process.run()
    return process.get_output_value("xas_obj", None)


class Larch_xftf(
    Process,
    name="xftf",
    input_names=["xas_obj"],
    optional_input_names=["xftf_config"],
    output_names=["xas_obj"],
):
    def run(self):
        xas_obj = self.inputs.xas_obj
        _xas_obj = self.getXasObject(xas_obj=xas_obj)

        self._advancement.reset(max_=_xas_obj.n_spectrum)
        self._advancement.startProcess()
        self._pool_process(xas_obj=_xas_obj)
        self._advancement.endProcess()
        self.outputs.xas_obj = _xas_obj

    def _pool_process(self, xas_obj):
        assert isinstance(xas_obj, XASObject)
        xftf_config = self.get_input_value("xftf_config", dict())
        n_s = len(xas_obj.spectra.data.flat)
        for i_s, spectrum in enumerate(xas_obj.spectra):
            process_spectr_xftf(
                spectrum=spectrum,
                configuration=xftf_config,
                callbacks=self.callbacks,
                overwrite=True,
            )
            self.progress = i_s / n_s * 100.0

    def definition(self):
        return "xftf calculation"

    def program_version(self):
        import larch.version

        return larch.version.version_data()["larch"]

    @staticmethod
    def program_name():
        return "larch_xftf"
