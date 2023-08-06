"""wrapper to the larch mback-norm process"""

from est.core.types import Spectrum, XASObject
from est.core.process.process import Process
from larch.xafs.mback import mback_norm
from larch.symboltable import Group
import logging

_logger = logging.getLogger(__name__)


def process_spectr_mback_norm(
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
    _logger.debug("start mback_norm on spectrum (%s, %s)" % (spectrum.x, spectrum.y))
    assert isinstance(spectrum, Spectrum)
    if not hasattr(spectrum, "norm"):
        _logger.error(
            "spectrum doesn't have norm. Maybe you meed to compute "
            "pre_edge first? Unable to compute mback_norm."
        )
        return None, None
    if not hasattr(spectrum, "pre_edge"):
        _logger.error(
            "spectrum doesn't have pre_edge. Maybe you meed to compute "
            "pre_edge first? Unable to compute mback_norm."
        )
        return None, None

    if not overwrite:
        spectrum = Spectrum.from_dict(spectrum.to_dict())
    _conf = configuration
    opts = {}

    spectrum.e0 = _conf.get("e0", None) or spectrum.e0
    for opt_name in (
        "z",
        "edge",
        "pre1",
        "pre2",
        "norm1",
        "norm2",
        "nnorm",
        "nvict",
    ):
        if opt_name in _conf:
            opts[opt_name] = _conf[opt_name]

    # Note: larch will calculate the pre-edge when missing
    res_group = Group()
    mback_norm(
        energy=spectrum.energy, mu=spectrum.mu, group=res_group, e0=spectrum.e0, **opts
    )
    spectrum.normalized_mu = res_group.norm
    if callbacks:
        for callback in callbacks:
            callback()
    return configuration, spectrum


def larch_mback_norm(xas_obj, **optional_inputs):
    """

    :param xas_obj: object containing the configuration and spectra to process
    :type: Union[XASObject, dict]
    :return: spectra dict
    :rtype: XASObject
    """
    process = Larch_mback_norm(inputs={"xas_obj": xas_obj, **optional_inputs})
    process.run()
    return process.get_output_value("xas_obj", None)


class Larch_mback_norm(
    Process,
    name="mback_norm",
    input_names=["xas_obj"],
    output_names=["xas_obj"],
    optional_input_names=["mback_norm_config", "mback_norm"],
):
    def run(self):
        xas_obj = self.inputs.xas_obj
        _xas_obj = self.getXasObject(xas_obj=xas_obj)

        self.progress = 0.0
        self._pool_process(xas_obj=_xas_obj)
        self.progress = 100.0
        self.outputs.xas_obj = _xas_obj

    def _pool_process(self, xas_obj):
        assert isinstance(xas_obj, XASObject)
        mback_norm_config = self.get_input_value("mback_norm_config", dict())
        n_s = len(xas_obj.spectra.data.flat)
        for i_s, spectrum in enumerate(xas_obj.spectra):
            process_spectr_mback_norm(
                spectrum=spectrum,
                configuration=mback_norm_config,
                callbacks=self.callbacks,
                overwrite=True,
            )
            self.progress = i_s / n_s * 100.0

    def definition(self):
        return "mback norm calculation"

    def program_version(self):
        import larch.version

        return larch.version.version_data()["larch"]

    @staticmethod
    def program_name():
        return "larch_mback_norm"
