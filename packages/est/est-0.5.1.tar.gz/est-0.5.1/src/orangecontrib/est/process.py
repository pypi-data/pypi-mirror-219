import logging
from ewoksorange.bindings.owwidgets import OWEwoksWidgetOneThread
from ewoksorange.bindings import ow_build_opts
from ewokscore.missing_data import is_missing_data
from est.core.types import XASObject

_logger = logging.getLogger(__file__)


class EstProcessWidget(OWEwoksWidgetOneThread, **ow_build_opts):
    want_control_area = False

    def handleNewSignals(self):
        self.task_input_changed()
        super().handleNewSignals()

    def task_input_changed(self):
        pass

    def task_output_changed(self):
        xas_obj = self.get_task_output_value("xas_obj")
        if is_missing_data(xas_obj):
            _logger.warning("no output data set. Unable to update the GUI")
            return
        elif isinstance(xas_obj, dict):
            xas_obj = XASObject.from_dict(xas_obj)

        if hasattr(self, "_window") and hasattr(self._window, "setXASObj"):
            self._window.setXASObj(xas_obj=xas_obj)
        elif hasattr(self, "_window") and hasattr(self._window, "xasObjViewer"):
            if hasattr(self._window.xasObjViewer, "setXASObj"):
                self._window.xasObjViewer.setXASObj(xas_obj=xas_obj)
