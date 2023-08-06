"""wrapper to the larch mback process"""

from est.core.types import Spectrum, XASObject
from est.core.process.process import Process
from larch.xafs.mback import mback
from larch.symboltable import Group
import logging

_logger = logging.getLogger(__name__)


def process_spectr_mback(
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
    _logger.debug("start mback on spectrum (%s, %s)" % (spectrum.x, spectrum.y))
    assert isinstance(spectrum, Spectrum)
    if spectrum.energy is None or spectrum.mu is None:
        _logger.error(
            "Energy and or Mu is/are not specified, unable to " "compute mback"
        )
        return None, None

    _conf = configuration
    opts = {}

    spectrum.e0 = _conf.get("e0", spectrum.e0)

    for opt_name in (
        "z",
        "edge",
        "pre1",
        "pre2",
        "norm1",
        "norm2",
        "order",
        "leexiang",
        "tables",
        "fit_erfc",
    ):
        if opt_name in _conf:
            opts[opt_name] = _conf[opt_name]
    if "z" not in opts:
        raise ValueError("atomic number of the absorber is not specify")

    if not overwrite:
        spectrum = Spectrum.from_dict(spectrum.to_dict())
    res_group = Group()
    mback(spectrum.energy, spectrum.mu, group=res_group, e0=spectrum.e0, **opts)

    spectrum.normalized_mu = res_group.norm
    if callbacks:
        for callback in callbacks:
            callback()
    return configuration, spectrum


def larch_mback(xas_obj, **optional_inputs):
    """

    :param xas_obj: object containing the configuration and spectra to process
    :type: Union[XASObject, dict]
    :return: spectra dict
    :rtype: XASObject
    """
    process = Larch_mback(inputs={"xas_obj": xas_obj, **optional_inputs})
    process.run()
    return process.get_output_value("xas_obj", None)


class Larch_mback(
    Process,
    name="mback",
    input_names=["xas_obj"],
    optional_input_names=["mback_config"],
    output_names=["xas_obj"],
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
        mback_config = self.get_input_value("mback_config", dict())
        n_s = len(xas_obj.spectra.data.flat)
        for i_s, spectrum in enumerate(xas_obj.spectra):
            process_spectr_mback(
                spectrum=spectrum,
                configuration=mback_config,
                callbacks=self.callbacks,
                overwrite=True,
            )
            self.progress = i_s / n_s * 100.0

    def definition(self):
        return "mback calculation"

    def program_version(self):
        import larch.version

        return larch.version.version_data()["larch"]

    @staticmethod
    def program_name():
        return "larch_mback"
