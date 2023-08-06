from functools import partial
from typing import Optional, Dict, List, Union, Tuple

import numpy as np
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QAction, \
    QFileDialog, QMessageBox
from numpy.typing import ArrayLike, NDArray

import primawera.lut as lut
from primawera.filters import linear_contrast, gamma_correction, linear_stretch
from primawera.loading import load_data
from primawera.modeutils import is_mode_color, is_mode_grayscale
from primawera.widgets.informationwindow import InformationWindow
from primawera.widgets.previewwindow import PreviewDialog


class CanvasBase(QWidget):
    """
    Base class for all the various widget. It itself does not represent any
    single view, but it contains a lot of the shared code.
    """
    menus_changed_signal = pyqtSignal()  # when menu changes
    signal_changed_filter = pyqtSignal(str)  # when filter changes
    signal_changed_coordinates = pyqtSignal(int, int, int, object, object,
                                            object)  # current coordinates

    def __init__(self, data: ArrayLike, mode: str,
                 desktop_height: int, desktop_width: int,
                 filters: Optional[Dict[str, bool]] = None,
                 filters_options: Optional[Dict[str, int]] = None,
                 overlay_data: Optional[NDArray[int]] = None,
                 overlay_is_grayscale: bool = True,
                 *args, **kwargs) -> None:
        """
        Constructs the object
        Parameters
        ----------
        data: ArrayLike
            Data to visualise. Has to be in the format (frames, width, height,
            channels). The last dimension is voluntary.
        mode: string
            Name of the image mode.
        desktop_height: int
            Height of the desktop.
        desktop_width: int
            Width of the desktop.
        filters: dictionary of (str, int) pairs, optional
            Describes the name of the filter to use. Deprecated
        filters_options: dictionary of (str, int), optional
            Parameters for the filters. Deprecated.
        overlay_data: integer ndarray, optional
            Data to overlay on top.
        overlay_is_grayscale: bool
            Is the overlay data grayscale?
        """
        super(CanvasBase, self).__init__(*args, **kwargs)
        self.data = np.asanyarray(data)
        if overlay_data is not None \
                and self._check_overlay_dtype(overlay_data,
                                              overlay_is_grayscale):
            self.raw_overlay_data = overlay_data
        elif overlay_data is not None:
            QMessageBox.information(
                self, "Information",
                "Could not safely convert the overlay's type to a suitable"
                "format. Note that while any bit long integer grayscale data "
                "is supported, coloured overlays can only use 8bit integers."
                f"Supplied overlay data (with type={overlay_data.dtype}) will"
                " be ignored.",
                buttons=QMessageBox.Ok,
                defaultButton=QMessageBox.Ok)
            self.raw_overlay_data = None
        else:
            self.raw_overlay_data = None

        self.overlay_is_grayscale = overlay_is_grayscale
        self.filters = filters
        self.filters_options = filters_options
        self.lut = None
        self.mode = mode
        self._showing_info_panel = False
        # This may change, for example when applying LUTs.
        self.mode_visualisation = mode
        self.preview_dialog_value = 0
        self.current_filter_name = None

        self.axes_orientation = (0, 1, 2)
        self.desktop_height = desktop_height
        self.desktop_width = desktop_width
        if self.mode == "":
            raise RuntimeError("Empty mode encountered")

    def _init_interface(self):
        """Initialises interface."""
        self.main_layout = QVBoxLayout()
        self.view_layout = QGridLayout()
        self._information_window = InformationWindow()
        self._information_window.update_data_format(self.data.shape,
                                                    self.data.dtype, self.mode)
        self._information_window.hide()
        self.signal_changed_filter.connect(
            self._information_window.update_filter_name_slot)

    def _create_actions(self):
        """Creates all QAction objects."""
        self.no_filter_action = QAction("None")
        self.logarithm_stretch_action = QAction("Logarithm stretch")
        self.linear_stretch_action = QAction("Linear stretch")
        self.linear_contrast_action = QAction("Linear contrast...")
        self.gamma_correction_action = QAction("Gamma correction...")
        self.lut_actions = []
        self.lut_actions.append(("None", QAction("None")))
        for lut_name in lut.LUTS.keys():
            self.lut_actions.append((lut_name, QAction(lut_name)))
        self.show_info_action = QAction("Show info panel")
        self.add_overlay_action = QAction("Add file as overlay...")
        self.remove_overlay_action = QAction("Remove overlay")

    def _connect_info_window_and_canvas(self):
        """Connect behaviour between information panel and canvas."""
        raise NotImplementedError("CanvasBase should not be directly created!")

    def _connect_actions(self):
        """Connects QActions to methods."""
        self.no_filter_action.triggered.connect(self._no_filter)
        self.logarithm_stretch_action.triggered.connect(
            self._logarithm_stretch)
        self.linear_stretch_action.triggered.connect(self._linear_stretch)
        self.linear_contrast_action.triggered.connect(self._linear_contrast)
        self.gamma_correction_action.triggered.connect(self._gamma_correction)
        for lut_name, lut_action in self.lut_actions:
            lut_action.triggered.connect(partial(self._apply_lut, lut_name))
        self._connect_info_window_and_canvas()
        self.signal_changed_coordinates.connect(
            self._information_window.update_coordinates_slot)
        self.show_info_action.triggered.connect(self._toggle_information_panel)
        self.add_overlay_action.triggered.connect(self._add_overlay_ui)
        self.remove_overlay_action.triggered.connect(self._remove_overlay)

    def _set_actions_checkable(self) -> None:
        """Set all QActions as checkable."""
        for action in self.get_actions():
            action.setCheckable(True)

    def _no_filter(self):
        """Disable filters."""
        self.current_filter_name = "No filter"
        self.filters.clear()
        self._redraw(self._process_data())

    def _linear_stretch(self):
        """Apply linear stretch."""
        self.current_filter_name = "Linearly stretched"
        self.filters = {"linear_stretch": True}
        self._redraw(self._process_data())

    def _logarithm_stretch(self):
        """Logarithmically stretch."""
        self.current_filter_name = "Logarithmically stretched"
        self.filters = {"logarithm_stretch": True}
        self._redraw(self._process_data())

    def _linear_contrast(self):
        """Linearly stretch the contrast."""
        self.current_filter_name = "Linearly adjusted contrast"
        dialog = PreviewDialog(self.data, [("Factor", int, 100, 0, 1)],
                               self.mode, linear_contrast)
        dialog.return_signal.connect(self.preview_dialog_slot)
        ret = dialog.exec()
        if ret == 0:
            self.no_filter_action.trigger()
            return
        factor = self.preview_dialog_value
        self.filters = {"linear_contrast": True}
        self.filters_options = {"factor": float(factor)}
        self._redraw(self._process_data())

    def _gamma_correction(self):
        """Gamma correct image."""
        self.current_filter_name = "Gamma corrected"
        dialog = PreviewDialog(self.data, [("Factor", float, 2.0, 0.0, 0.1)],
                               self.mode, gamma_correction)
        dialog.return_signal.connect(self.preview_dialog_slot)
        ret = dialog.exec()
        if ret == 0:
            self.no_filter_action.trigger()
            return
        factor = self.preview_dialog_value
        self.filters = {"gamma_correction": True}
        self.filters_options = {"factor": factor}
        self._redraw(self._process_data())

    def _apply_lut(self, name):
        """Apply a LUT with the given name."""
        if name == "None":
            self.mode_visualisation = self.mode
            self.lut = None
        else:
            self.lut = lut.get_lut(name)
        self._redraw(self._process_data())

    def _check_overlay_dtype(self, overlay: NDArray,
                             is_overlay_grayscale: bool) -> bool:
        """Check of overlay is castable to integer type."""
        if is_overlay_grayscale:
            # We can linearly stretch it later
            return np.can_cast(overlay.dtype, int)

        # Overlay contains RGB data
        return np.can_cast(overlay.dtype, np.uint8)

    def _add_overlay_io(self) -> Optional[Tuple[ArrayLike, bool]]:
        """Opens the file dialog for choosing overlay file."""
        file_name, _ = QFileDialog.getOpenFileName(self, "Open file", ".",
                                                   "Image file (*.jpg *.png"
                                                   " *.h5 *.tif *.tiff)")
        if file_name == "":
            # User did not select a file
            return
        try:
            data, mode = load_data(file_name)
            if is_mode_color(mode):
                is_grayscale = False
            elif is_mode_grayscale(mode):
                is_grayscale = True
            else:
                raise RuntimeError("Cannot determine if the data is grayscale"
                                   f"or colored! Modes is {mode}!")
            if not self._check_overlay_dtype(data, is_grayscale):
                raise RuntimeError(
                    f"Cannot safely cast {data.dtype} to an unsigned 8 bit "
                    f"integer!")
        except RuntimeError as err:
            QMessageBox.critical(self, "Error",
                                 f"Failed to load data ({file_name}) "
                                 f"with message: {err}",
                                 buttons=QMessageBox.Ok,
                                 defaultButton=QMessageBox.Ok)
            return None
        return data, is_grayscale

    def _reshape_overlay_data(self, overlay_data: NDArray[int],
                              is_grayscale: bool) -> NDArray[int]:
        """Reshapes overlay data to the correct format."""
        overlay_dims = len(overlay_data.shape)

        if is_grayscale and overlay_dims == 2:
            w, h = overlay_data.shape
            overlay_data = np.reshape(overlay_data, (1, w, h))
            overlay_dims = len(overlay_data.shape)
            assert overlay_dims == 3
        elif not is_grayscale and overlay_dims == 3:
            w, h, ch = overlay_data.shape
            overlay_data = np.reshape(overlay_data, (1, w, h, ch))
            overlay_dims = len(overlay_data.shape)
            assert overlay_dims == 4

        if is_grayscale and overlay_dims == 3:
            # Rescale labels for visualisation purposes
            overlay_data = np.array(255.0 * linear_stretch(overlay_data),
                                    dtype=np.uint8)

            # Reshape
            f, w, h = overlay_data.shape
            overlay_data = np.reshape(overlay_data, (f, w, h, 1))
            orig_overlay = overlay_data
            overlay_data = np.append(overlay_data, overlay_data, axis=3)
            overlay_data = np.append(overlay_data, orig_overlay, axis=3)
            overlay_dims = len(overlay_data.shape)
            assert overlay_dims == 4, "Reshaping overlay into higher" \
                                      " dimension failed!"

        assert overlay_dims == 4, "Reshaping failed due to incorrect " \
                                  "internal logic. Please contact the " \
                                  "developer."
        return overlay_data

    def _add_overlay_ui(self) -> None:
        """UI for the add overlay action."""
        result = self._add_overlay_io()
        if result is None:
            return

        overlay_data, is_grayscale = result
        self._add_overlay(overlay_data, is_grayscale)

    def _add_overlay_aux(self, overlay_data: NDArray[int],
                         is_grayscale: bool = True) -> Optional[NDArray[int]]:
        overlay_original = overlay_data
        overlay_reshaped = self._reshape_overlay_data(overlay_data,
                                                      is_grayscale)
        data_dims = len(self.data.shape)

        # The overlay can have more dimensions if it is coloured and the data
        # under it is in grayscale.
        if (data_dims == 3
            and overlay_reshaped.shape[:-1] != self.data.shape) \
                or (
                data_dims == 4 and overlay_reshaped.shape != self.data.shape):
            QMessageBox.critical(
                self, "Error",
                f"The shape {overlay_original.shape} is not compatible "
                f"with underlying image {self.data.shape}. It was "
                f"automatically reshaped to {overlay_reshaped.shape}",
                buttons=QMessageBox.Ok,
                defaultButton=QMessageBox.Ok)
            return

        opacity_mask_shape = list(overlay_reshaped.shape)
        opacity_mask_shape[-1] = 1
        opacity_mask = np.zeros(shape=tuple(opacity_mask_shape)).astype(
            np.uint8)
        opacity_mask[overlay_reshaped[:, :, :, 0] != 0] = 255

        # Add opacity (alpha channel) to the overlay data
        overlay_reshaped = np.append(overlay_reshaped, opacity_mask, axis=3)
        return overlay_reshaped

    def _add_overlay(self, overlay_data: NDArray[int],
                     is_grayscale: bool = True) -> None:
        """Add overlay."""
        raise NotImplementedError("CanvasBase should not be directly created!")

    def _remove_overlay(self) -> None:
        """Removes overlay."""
        raise NotImplementedError("CanvasBase should not be directly created!")

    def _redraw(self, new_data) -> None:
        """Updates and redraws the canvas."""
        raise NotImplementedError("CanvasBase should not be directly created!")

    def keyPressEvent(self, event: QKeyEvent) -> None:
        actions = [
            (QtCore.Qt.Key_Plus, self._increase_zoom_level),
            (QtCore.Qt.Key_Minus, self._decrease_zoom_level),
            (QtCore.Qt.Key_I, self._toggle_information_panel),
            (QtCore.Qt.Key_Space, self._hide_overlay)
        ]

        entered_actions = list(
            filter(lambda comb: comb[0] == event.key(), actions))
        if len(entered_actions) == 0:
            event.ignore()
            return
        _, action = entered_actions[0]
        action()

    def keyReleaseEvent(self, event) -> None:
        if event.isAutoRepeat():
            event.ignore()
        elif event.key() == QtCore.Qt.Key_Space:
            self._show_overlay()
            event.accept()
        else:
            event.ignore()

    def _increase_zoom_level(self):
        """Increases zoom level."""
        raise NotImplementedError("CanvasBase should not be directly created!")

    def _decrease_zoom_level(self):
        """Decreases zoom level."""
        raise NotImplementedError("CanvasBase should not be directly created!")

    def _toggle_information_panel(self):
        self._showing_info_panel = not self._showing_info_panel
        if not self._showing_info_panel:
            self._information_window.hide()
        else:
            self._information_window.show()

    def get_filters(self):
        """Returns all possible filters as a list of QActions."""
        raise NotImplementedError("CanvasBase should not be directly created!")

    def get_luts(self):
        """Returns all possible LUT QActions as a list."""
        raise NotImplementedError("CanvasBase should not be directly created!")

    def get_actions(self):
        """Returns all possible QActions."""
        raise NotImplementedError("CanvasBase should not be directly created!")

    def get_menus(self):
        """Returns all menus."""
        return [
            ("Other", [self.show_info_action]),
        ]

    def _process_data(self):
        """Apply filters on data and emit the currently used filter name."""
        if self.current_filter_name is not None:
            self.signal_changed_filter.emit(self.current_filter_name)

    def update_desktop_size(self, width: int, height: int) -> None:
        """Update the desktop size."""
        self.desktop_width = width
        self.desktop_height = height

    @pyqtSlot(list)
    def preview_dialog_slot(self, data: List[Union[int, float]]) -> None:
        """Slot for taking the parameters chosen by user in the
        PreviewWindow."""
        self.preview_dialog_value = data[0]

    @pyqtSlot(int, int, int, list)
    def changed_coordinates_slot_emitter(self, frame: int, row: int, col: int,
                                         mapped_val: ArrayLike) -> None:
        """Emits the current coordinates under the cursor, its original value
        at those coordinates, the mapped value, and value of the overlay."""
        if self.raw_overlay_data is not None:
            chosen_coords = (frame, row, col)
            # Note: unlike the data, overlay data can have all sorts of shapes-
            # mainly (f, w, h, ch), (w, h, ch) or (f, w, h).
            # Since the signal always returns coordinates in the form (f, w, h)
            # we need to handle the (w, h, ch) case specially
            if not self.overlay_is_grayscale \
                    and len(self.raw_overlay_data.shape) == 3:
                chosen_coords = (row, col)

            overlay_label = self.raw_overlay_data[chosen_coords]
        else:
            overlay_label = None

        self.signal_changed_coordinates.emit(frame, row, col,
                                             mapped_val,
                                             self.data[frame, row, col],
                                             [overlay_label])

    def closeEvent(self, event) -> None:
        self._information_window.close()
        super().closeEvent(event)

    def _hide_overlay(self) -> None:
        """Hides the overlay temporarily."""
        raise NotImplementedError("CanvasBase should not be directly created!")

    def _show_overlay(self) -> None:
        """Shows the overlay."""
        raise NotImplementedError("CanvasBase should not be directly created!")
