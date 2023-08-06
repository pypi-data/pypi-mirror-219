"""wrapper to pymca `exafs` process"""

import logging
import numpy
from PyMca5.PyMcaPhysics.xas.XASClass import XASClass
from PyMca5.PyMcaPhysics.xas.XASClass import e2k
from est.core.process.process import Process

# from est.core.process.process import _NexusDatasetDef
from est.core.types import XASObject, Spectrum

_logger = logging.getLogger(__name__)


def process_spectr_exafs(
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
    _logger.debug("start exafs on spectrum (%s, %s)" % (spectrum.x, spectrum.y))
    if spectrum.energy is None or spectrum.mu is None:
        _logger.error(
            "Energy and or Mu is/are not specified, unable to " "compute exafs"
        )
        return None, None
    pymca_xas = XASClass()
    pymca_xas.setSpectrum(energy=spectrum.energy, mu=spectrum.mu)
    if configuration is not None:
        pymca_xas.setConfiguration(configuration)

    if spectrum.pre_edge is None:
        raise ValueError("No pre-edge computing yet. Please call normalization first")

    e0 = pymca_xas.calculateE0()
    ddict = {
        "Energy": pymca_xas._energy,
        "Mu": pymca_xas._mu,
    }
    ddict["Energy"] = pymca_xas._energy
    ddict["Mu"] = pymca_xas._mu
    cleanMu = pymca_xas._mu - spectrum.pre_edge
    kValues = e2k(pymca_xas._energy - e0)

    ddict.update(pymca_xas.postEdge(kValues, cleanMu))

    dataSet = numpy.zeros((cleanMu.size, 2), float)
    dataSet[:, 0] = kValues
    dataSet[:, 1] = cleanMu

    # exafs normalization
    if not overwrite:
        spectrum = Spectrum.from_dict(ddict=ddict)

    exafs = (cleanMu - ddict["PostEdgeB"]) / ddict["PostEdgeB"]
    # update the spectrum
    spectrum.k = kValues
    spectrum.chi = cleanMu
    if ddict["KWeight"]:
        exafs *= pow(kValues, ddict["KWeight"])
    spectrum.pymca_dict["PostEdgeB"] = ddict["PostEdgeB"]
    spectrum.pymca_dict["KMin"] = ddict["KMin"]
    spectrum.pymca_dict["KMax"] = ddict["KMax"]
    spectrum.pymca_dict["KnotsX"] = ddict["KnotsX"]
    spectrum.pymca_dict["KnotsY"] = ddict["KnotsY"]
    spectrum.pymca_dict["EXAFSNormalized"] = exafs

    if callbacks:
        for callback in callbacks:
            callback()

    if output is not None:
        assert output_dict is not None
        output[output_dict[spectrum]] = spectrum

    return configuration, spectrum


def pymca_exafs(xas_obj, **optional_inputs):
    """

    :param xas_obj: object containing the configuration and spectra to process
    :type: Union[XASObject, dict]
    :return: spectra dict
    :rtype: XASObject
    """
    process = PyMca_exafs(inputs={"xas_obj": xas_obj, **optional_inputs})
    process.run()
    return process.get_output_value("xas_obj", None)


class PyMca_exafs(
    Process,
    name="exafs",
    input_names=["xas_obj"],
    output_names=["xas_obj"],
    optional_input_names=["exafs"],
):
    """Process spectra for exafs and get information about the processing
    advancement"""

    def set_properties(self, properties):
        if "_pymcaSettings" in properties:
            self.setConfiguration(properties["_pymcaSettings"])

    def run(self):
        xas_obj = self.inputs.xas_obj
        if xas_obj is None:
            raise ValueError("xas_obj should be provided")
        _xas_obj = self.getXasObject(xas_obj=xas_obj)
        if self.inputs.exafs:
            self.setConfiguration(self.inputs.exafs)
            _xas_obj.configuration["EXAFS"] = self.inputs.exafs

        self.progress = 0.0
        self._pool_process(xas_obj=_xas_obj)
        self.progress = 100.0
        self._advancement.endProcess()
        self.outputs.xas_obj = _xas_obj

    def _pool_process(self, xas_obj):
        assert isinstance(xas_obj, XASObject)
        n_s = len(xas_obj.spectra.data.flat)
        for i_s, spectrum in enumerate(xas_obj.spectra.data.flat):
            assert (
                spectrum.pre_edge is not None
            ), "normalization has not been properly executed"
            process_spectr_exafs(
                spectrum=spectrum,
                configuration=xas_obj.configuration,
                callbacks=self.callbacks,
                overwrite=True,
            )
            self.progress = i_s / n_s * 100.0

    def definition(self):
        return "exafs calculation"

    def program_version(self):
        import PyMca5

        return PyMca5.version()

    @staticmethod
    def program_name():
        return "pymca_exafs"
