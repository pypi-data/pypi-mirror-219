from typing import Optional

from est.core.io import XASReader
from est.core.types import XASObject
from est.io.utils.information import InputInformation
from .process import Process


class DumpXasObject(
    Process,
    input_names=["xas_obj", "output_file"],
    output_names=["result"],
):
    @staticmethod
    def definition():
        return "write XAS object to a file"

    def run(self):
        xas_object = self.inputs.xas_obj
        if xas_object is None:
            raise ValueError("xas_obj should be provided")
        if isinstance(xas_object, dict):
            xas_object = XASObject.from_dict(xas_object)
        if not isinstance(xas_object, XASObject):
            raise TypeError(
                "xas_object should be a convertable dict or an" "instance of XASObject"
            )

        xas_object.dump(self.output_file)
        self.outputs.result = self.output_file

    @property
    def output_file(self) -> Optional[str]:
        if self.missing_inputs.output_file:
            return None
        return self.inputs.output_file


class ReadXasObject(
    Process,
    name="read xas",
    output_names=["xas_obj"],
    input_names=["input_information"],
):
    @staticmethod
    def definition():
        return "read XAS data from file"

    def run(self):
        self.setConfiguration(self.inputs.input_information)
        input_information = InputInformation.from_dict(self.inputs.input_information)
        xas_obj = XASReader.read_frm_url(input_information)
        self.outputs.xas_obj = xas_obj
