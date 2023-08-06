"""contains `energy roi` related functions / classes"""

from est.core.types.xasobject import XASObject
from .process import Process


def xas_energy_roi(xas_obj):
    """
    apply roi on the XASObject.spectra

    :param xas_obj: object containing the configuration and spectra to process
    :type: Union[:class:`.XASObject`, dict]
    :return: spectra dict
    :rtype: :class:`.XASObject`
    """
    process = EnergyROIProcess(inputs={"xas_obj": xas_obj})
    process.run()
    return process.get_output_value("xas_obj", None)


class EnergyROIProcess(
    Process,
    name="energy roi",
    input_names=["xas_obj"],
    optional_input_names=["energy_roi"],
    output_names=["xas_obj"],
):
    @staticmethod
    def program_name():
        return "energy-roi"

    def definition(self):
        return "apply a ROI on energy range"

    def run(self):
        """

        :param xas_obj: object containing the configuration and spectra to process
        :type: Union[:class:`.XASObject`, dict]
        :return: spectra dict
        :rtype: :class:`.XASObject`
        """
        xas_obj = self.inputs.xas_obj
        _xas_obj = self.getXasObject(xas_obj=xas_obj)
        assert isinstance(_xas_obj, XASObject)

        energy_roi = self.get_input_value("energy_roi", dict())

        self.progress = 0.0
        self._apply_roi(_xas_obj, energy_roi.get("minE"), energy_roi.get("maxE"))
        self.progress = 100.0

        self.outputs.xas_obj = _xas_obj

    def _apply_roi(self, xas_obj, emin, emax):
        if emin is None and emax is None:
            return
        if emin is None:
            mask = xas_obj.spectra.energy <= emax
        elif emax is None:
            mask = xas_obj.spectra.energy >= emin
        else:
            mask = (xas_obj.spectra.energy <= emax) & (xas_obj.spectra.energy >= emin)

        xas_obj.spectra.energy = xas_obj.spectra.energy[mask]
        n_s = len(xas_obj.spectra.data.flat)
        for i_s, spectrum in enumerate(xas_obj.spectra.data.flat):
            spectrum.energy = spectrum.energy[mask]
            spectrum.mu = spectrum.mu[mask]
            for attached_key in ("I0", "I1", "I2", "mu_ref"):
                if hasattr(spectrum, attached_key):
                    values = getattr(spectrum, attached_key)[mask]
                    setattr(spectrum, attached_key, values)
            self.progress = i_s / n_s * 100.0
