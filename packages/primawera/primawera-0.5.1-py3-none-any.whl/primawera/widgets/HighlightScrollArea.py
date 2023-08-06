"""
This module contains the custom QScrollArea class used for visualisng pixmap
data.
"""
from PyQt5.QtWidgets import QScrollArea


class HighlightScrollArea(QScrollArea):
    """
    Custom QScrollArea widget. If the widget has focus, then it has a yellow
    border.
    """

    def __init__(self, width: int = 1):
        """
        Constructor.

        Parameters
        ----------
        width: int
            Width of the border.
        """
        super(HighlightScrollArea, self).__init__()
        if self.hasFocus():
            self.setStyleSheet(
                f"border: {width}px solid yellow; padding: 0px; margin: 0px;")
        else:
            self.setStyleSheet(
                f"border: {width}px solid gray; padding: 0px; margin: 0px;")
        self.setMouseTracking(True)
        self._width = width

    def focusInEvent(self, event):
        self.setStyleSheet(f"border: {self._width}px solid yellow;"
                           f" padding: 0px; margin: 0px;")
        event.accept()

    def focusOutEvent(self, event):
        self.setStyleSheet(
            f"border: {self._width}px solid gray; padding: 0px; margin: 0px;")
        event.accept()

    def in_focus(self) -> bool:
        return self.hasFocus()
