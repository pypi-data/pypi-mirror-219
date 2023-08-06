"""module for process base class"""

import logging
from ewokscore.taskwithprogress import TaskWithProgress as Task
from est.core.types import XASObject
from .progress import Progress
from ..utils import extract_properties_from_dict
from ... import __version__

_logger = logging.getLogger(__name__)


class Process(Task, register=False):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._advancement = Progress(name=self.name)
        self.__stop = False
        """flag to notice when a end of process is required"""
        self._settings = {}
        # configuration
        self._callbacks = []

    def __init_subclass__(subclass, name="", **kwargs):
        super().__init_subclass__(**kwargs)
        subclass._NAME = name

    @property
    def name(self) -> str:
        return self._NAME

    def stop(self):
        self.__stop = True

    @property
    def advancement(self):
        return self._advancement

    @advancement.setter
    def advancement(self, advancement):
        assert isinstance(advancement, Progress)
        self._advancement = advancement

    @property
    def callbacks(self):
        return self._callbacks

    @staticmethod
    def getXasObject(xas_obj) -> XASObject:
        if isinstance(xas_obj, dict):
            _xas_obj = XASObject.from_dict(xas_obj)
        else:
            _xas_obj = xas_obj
        assert isinstance(_xas_obj, XASObject)
        if _xas_obj.n_spectrum > 0:
            _xas_obj.spectra.check_validity()
        assert isinstance(_xas_obj, XASObject)
        return _xas_obj

    def program_name(self) -> str:
        """
        :return: name of the process to be saved in HDF5
        :rtype: dict
        """
        return self.class_registry_name().split(".")[-1]

    @staticmethod
    def program_version() -> str:
        """
        :return: version of the process to be saved in HDF5
        :rtype: dict
        """
        return __version__

    @staticmethod
    def definition(self) -> str:
        """
        :return: definition of the process to be saved in HDF5
        :rtype: dict
        """
        raise NotImplementedError("Base class")

    def getConfiguration(self) -> dict:
        """
        :return: parameters of the process to be saved in HDF5
        :rtype: dict
        """
        if len(self._settings) > 0:
            return self._settings
        else:
            return None

    def setConfiguration(self, configuration: dict):
        # filter configuration from orange widgets
        if "__version__" in configuration:
            del configuration["__version__"]
        if "savedWidgetGeometry" in configuration:
            del configuration["savedWidgetGeometry"]
        if "savedWidgetGeometry" in configuration:
            del configuration["savedWidgetGeometry"]
        if "controlAreaVisible" in configuration:
            del configuration["controlAreaVisible"]

        self._settings = configuration

    def addCallback(self, callback):
        self._callbacks.append(callback)

    def update_properties(self, properties):
        if properties is None:
            return
        if isinstance(properties, str):
            properties = extract_properties_from_dict(properties)
        self._settings.update(properties)
