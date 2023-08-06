"""
This module is used to manage the rsync between files for transfert.
"""

from AnyQt.QtWidgets import QApplication
from AnyQt.QtCore import Qt, QUrl, QEvent, pyqtSignal as Signal
from est.core.utils.designpattern import singleton

# TODO: this should be removed


@singleton
class QApplicationManager(QApplication):
    """Return a singleton on the CanvasApplication"""

    fileOpenRequest = Signal(QUrl)

    def __init__(self):
        QApplication.__init__(self, [])
        self.setAttribute(Qt.AA_DontShowIconsInMenus, True)

    def event(self, event):
        if event.type() == QEvent.FileOpen:
            self.fileOpenRequest.emit(event.url())

        return QApplication.event(self, event)
