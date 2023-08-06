"""wrapper to the larch autobk process"""

from est.core.types import Spectrum, XASObject
from est.core.process.process import Process
from larch.xafs.autobk import autobk
from larch.symboltable import Group
import logging

_logger = logging.getLogger(__name__)


def process_spectr_autobk(
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
    _logger.debug("start autobk on spectrum (%s, %s)" % (spectrum.x, spectrum.y))
    assert isinstance(spectrum, Spectrum)
    if spectrum.energy is None or spectrum.mu is None:
        _logger.error("Energy and or Mu is/are not specified, unable to compute autpbk")
        return None, None

    _conf = configuration
    # keep "edge_step" and "e0" up to data
    spectrum.edge_step = _conf.get("edge_step", None) or spectrum.edge_step
    spectrum.e0 = _conf.get("e0", None) or spectrum.e0

    opts = {}
    for opt_name in (
        "rbkg",
        "nknots",
        "kmin",
        "kmax",
        "kweight",
        "dk",
        "win",
        "k_std",
        "chi_std",
        "nfft",
        "kstep",
        "pre_edge_kws",
        "nclamp",
        "clamp_lo",
        "clamp_hi",
        "calc_uncertainties",
        "err_sigma",
    ):
        if opt_name in _conf:
            opts[opt_name] = _conf[opt_name]
    if spectrum.edge_step is not None:
        _conf["pre_edge_kws"] = spectrum.edge_step

    if not overwrite:
        spectrum = Spectrum.from_dict(spectrum.to_dict())

    res_group = Group()
    autobk(
        energy=spectrum.energy,
        mu=spectrum.mu,
        group=res_group,
        edge_step=spectrum.edge_step,
        e0=spectrum.e0,
        **opts
    )
    spectrum.e0 = res_group.e0
    spectrum.chi = res_group.chi
    spectrum.k = res_group.k
    spectrum.larch_dict["bkg"] = res_group.bkg

    if callbacks:
        for callback in callbacks:
            callback()
    return configuration, spectrum


def larch_autobk(xas_obj, **optional_inputs):
    """

    :param xas_obj: object containing the configuration and spectra to process
    :type: Union[XASObject, dict]
    :return: spectra dict
    :rtype: XASObject
    """
    process = Larch_autobk(inputs={"xas_obj": xas_obj, **optional_inputs})
    process.run()
    return process.get_output_value("xas_obj", None)


class Larch_autobk(
    Process,
    name="autobk",
    input_names=["xas_obj"],
    optional_input_names=["autobk_config"],
    output_names=["xas_obj"],
):
    def run(self):
        xas_obj = self.inputs.xas_obj
        _xas_obj = self.getXasObject(xas_obj=xas_obj)

        self.progress = 0
        self._pool_process(xas_obj=_xas_obj)
        self.progress = 100
        self.outputs.xas_obj = _xas_obj

    def _pool_process(self, xas_obj):
        assert isinstance(xas_obj, XASObject)
        autobk_config = self.get_input_value("autobk_config", dict())
        n_s = len(xas_obj.spectra.data.flat)
        for i_s, spectrum in enumerate(xas_obj.spectra):
            process_spectr_autobk(
                spectrum=spectrum,
                configuration=autobk_config,
                callbacks=self.callbacks,
                overwrite=True,
            )
            self.progress = i_s / n_s * 100.0

    def definition(self):
        return "autobk calculation"

    def program_version(self):
        import larch.version

        return larch.version.version_data()["larch"]

    @staticmethod
    def program_name():
        return "larch_autobk"
