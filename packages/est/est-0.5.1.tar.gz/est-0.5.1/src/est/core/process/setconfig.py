from .process import Process


def _xas_set_config(xas_obj):
    """
    Copy process configuration to object

    :param xas_obj: object containing the configuration and spectra to process
    :type: Union[:class:`.XASObject`, dict]
    :return: spectra dict
    :rtype: :class:`.XASObject`
    """
    xas_set_config = _SetConfigProcess()
    return xas_set_config.process(xas_obj=xas_obj)


class _SetConfigProcess(Process, name="set_config"):
    def process(self, xas_obj):
        """

        :param xas_obj: object containing the configuration and spectra to process
        :type: Union[:class:`.XASObject`, dict]
        :return: spectra dict
        :rtype: :class:`.XASObject`
        """
        assert xas_obj is not None
        _xas_obj = self.getXasObject(xas_obj=xas_obj)
        conf_obj = _xas_obj.configuration
        conf_process = self.getConfiguration()
        for key, value in conf_process.items():
            conf_obj[key] = value
        _xas_obj.configuration = conf_obj
        return _xas_obj
