"""wrapper to the larch pre-edge process"""

from est.core.types import Spectrum, XASObject
from est.core.process.process import Process
from larch.xafs.pre_edge import pre_edge
import logging
from larch.symboltable import Group

_logger = logging.getLogger(__name__)


def process_spectr_pre_edge(
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
    :param callbacks: callbacks to execute.
    :param output: list to store the result, needed for pool processing
    :type: multiprocessing.manager.list
    :param output_dict: key is: input spectrum, value is index in the output
                        list.
    :type: dict
    :return: processed spectrum
    :rtype: tuple (configuration, spectrum)
    """
    _logger.debug("start pre_edge on spectrum (%s, %s)" % (spectrum.x, spectrum.y))
    assert isinstance(spectrum, Spectrum)
    if spectrum.energy is None or spectrum.mu is None:
        _logger.error(
            "Energy and or Mu is/are not specified, unable to " "compute pre edge"
        )
        return None, None
    _conf = configuration

    spectrum.e0 = _conf.get("e0", None) or spectrum.e0

    opts = {}
    for opt_name in (
        "z",
        "edge",
        "pre1",
        "pre2",
        "norm1",
        "nnorm",
        "nvict",
        "step",
        "make_flat",
        "norm2",
        "order",
        "leexiang",
        "tables",
        "fit_erfc",
    ):
        if opt_name in _conf:
            opts[opt_name] = _conf[opt_name]

    if not overwrite:
        spectrum = Spectrum.from_dict(spectrum=spectrum)

    res_group = Group()
    pre_edge(
        energy=spectrum.energy, mu=spectrum.mu, group=res_group, e0=spectrum.e0, **opts
    )
    spectrum.e0 = res_group.e0
    spectrum.normalized_mu = res_group.norm
    spectrum.flatten_mu = res_group.flat
    spectrum.pre_edge = res_group.pre_edge
    spectrum.post_edge = res_group.post_edge
    spectrum.edge_step = res_group.edge_step

    if callbacks:
        for callback in callbacks:
            callback()
    return configuration, spectrum


def larch_pre_edge(xas_obj, **optional_inputs):
    """

    :param xas_obj: object containing the configuration and spectra to process
    :type: Union[XASObject, dict]
    :return: spectra dict
    :rtype: XASObject
    """
    process = Larch_pre_edge(inputs={"xas_obj": xas_obj, **optional_inputs})
    process.run()
    return process.get_output_value("xas_obj", None)


class Larch_pre_edge(
    Process,
    name="pre_edge",
    input_names=["xas_obj"],
    optional_input_names=["pre_edge_config"],
    output_names=["xas_obj"],
):
    def run(self):
        xas_obj = self.inputs.xas_obj
        if xas_obj is None:
            raise ValueError("xas_obj should be provided")
        self._xas_obj = self.getXasObject(xas_obj=xas_obj)
        _xas_obj = self._xas_obj

        self.progress = 0.0
        self._pool_process(xas_obj=_xas_obj)
        self.progress = 100.0
        self.outputs.xas_obj = _xas_obj

    def _pool_process(self, xas_obj):
        assert isinstance(xas_obj, XASObject)
        pre_edge_config = self.get_input_value("pre_edge_config", dict())
        n_s = len(xas_obj.spectra.data.flat)
        for i_s, spectrum in enumerate(xas_obj.spectra):
            process_spectr_pre_edge(
                spectrum=spectrum,
                configuration=pre_edge_config,
                callbacks=self.callbacks,
                overwrite=True,
            )
            self.progress = i_s / n_s * 100.0

    def definition(self):
        return "pre_edge calculation"

    def program_version(self):
        import larch.version

        return larch.version.version_data()["larch"]

    @staticmethod
    def program_name():
        return "larch_pre_edge"
