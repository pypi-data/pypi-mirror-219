from typing import Dict, List, Tuple, Optional

import numpy as np
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QAction
from numpy.typing import ArrayLike, NDArray

from primawera.filters import linear_stretch, gamma_correction, \
    linear_contrast, logarithm_stretch
from primawera.lut import apply_lut
from primawera.widgets.canvasbase import CanvasBase
from primawera.widgets.visualiser import Visualiser


class Canvas2D(CanvasBase):
    """
    Basic view of 2D image data.
    """
    menus_changed_signal = pyqtSignal()

    def __init__(self, data: ArrayLike, mode: str,
                 desktop_height: int, desktop_width: int,
                 filters: Optional[Dict[str, bool]] = None,
                 filters_options: Optional[Dict[str, int]] = None,
                 overlay_data: Optional[NDArray[int]] = None,
                 overlay_is_grayscale: bool = True,
                 *args, **kwargs) -> None:
        """
        Constructs the object.
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
            Describes the name of the filter to use.
        filters_options: dictionary of (str, int), optional
            Parameters for the filters.
        overlay_data: integer ndarray, optional
            Data to overlay on top.
        overlay_is_grayscale: bool
            Is the overlay data grayscale?
        """
        super(Canvas2D, self).__init__(data, mode, desktop_height,
                                       desktop_width, filters, filters_options,
                                       overlay_data, overlay_is_grayscale,
                                       *args, **kwargs)
        self._init_interface()
        self._create_actions()
        self._set_actions_checkable()
        self._connect_actions()

        if self.raw_overlay_data is not None:
            self._add_overlay(self.raw_overlay_data, self.overlay_is_grayscale)

        if self.mode != 'F':
            self._no_filter()
        else:
            self._linear_stretch()

        # Check default options
        self.get_filters()[0].setChecked(True)
        if self.mode == "grayscale":
            self.get_luts()[0].setChecked(True)

    def _process_data(self) -> ArrayLike:
        super()._process_data()
        if self.mode == "1":
            return (self.data * 255).astype(np.uint8)
        processed_data = self.data.astype(float)

        # Apply filters
        if self.filters.get("linear_stretch", False):
            processed_data = 255.0 * linear_stretch(processed_data)
        elif self.filters.get("gamma_correction", False):
            gamma_factor = self.filters_options.get("factor", 0.5)
            processed_data = gamma_correction(processed_data, gamma_factor)
        elif self.filters.get("linear_contrast", False):
            stretch_factor = self.filters_options.get("factor", 2)
            processed_data = linear_contrast(processed_data, stretch_factor)
        elif self.filters.get("logarithm_stretch", False):
            processed_data = logarithm_stretch(processed_data, factor=10.0)
            # Normalise to range [0,255]
            processed_data = 255.0 * linear_stretch(processed_data)

        # Clip data
        processed_data = np.clip(processed_data, 0, 255.0).astype(np.uint8)

        # Apply LUT
        if self.lut is not None:
            self.mode_visualisation = "rgb"
            processed_data = apply_lut(processed_data, self.lut)

        self.menus_changed_signal.emit()
        return processed_data

    def _init_interface(self) -> None:
        super()._init_interface()

        maximum_width = int(self.desktop_width * 0.80)
        maximum_height = int(self.desktop_height * 0.80)
        processed_data = self._process_data()
        self.visualiser = Visualiser(processed_data, (0, 1, 2), self.mode,
                                     maximum_height, maximum_width, True)

        self.view_layout.addWidget(self.visualiser, 0, 0, Qt.AlignTop)
        self.main_layout.addLayout(self.view_layout)
        self.setLayout(self.main_layout)
        self._connect_info_window_and_canvas()

    def _connect_info_window_and_canvas(self) -> None:
        self.visualiser.signal_position.connect(
            self.changed_coordinates_slot_emitter)

    def get_actions(self) -> List[QAction]:
        result = self.get_filters()
        result.extend(self.get_luts())
        return result

    def get_filters(self) -> List[QAction]:
        if self.mode == "F":
            return [self.linear_stretch_action, self.logarithm_stretch_action]

        result = [self.no_filter_action]
        if self.mode == "1":
            return result

        if self.mode == "grayscale" or self.mode == "F":
            result.append(self.linear_stretch_action)

        result.extend([self.linear_contrast_action,
                       self.gamma_correction_action])
        return result

    def get_luts(self) -> List[QAction]:
        if self.mode == "grayscale" or self.mode == "F":
            return [action for _, action in self.lut_actions]
        return []

    def get_menus(self) -> List[Tuple[str, List[QAction]]]:
        base_menu = super().get_menus()
        lut_entry = ("LUT", self.get_luts())
        filter_entry = ("Filters", self.get_filters())
        overlay_entry = "Overlay", [self.add_overlay_action,
                                    self.remove_overlay_action],
        result = [filter_entry, lut_entry, overlay_entry] if lut_entry[1] \
            else [filter_entry, overlay_entry]
        return result + base_menu

    def _redraw(self, new_data: ArrayLike) -> None:
        self.visualiser.update_data(new_data, self.axes_orientation,
                                    self.mode_visualisation)
        self.visualiser.redraw()

    def _increase_zoom_level(self):
        self.visualiser.increase_zoom_level()

    def _decrease_zoom_level(self):
        self.visualiser.decrease_zoom_level()

    def _add_overlay(self, overlay_data: NDArray[int],
                     is_grayscale: bool = True) -> None:
        overlay_reshaped = self._add_overlay_aux(overlay_data, is_grayscale)
        if overlay_reshaped is None:
            return  # Failed to use the overlay data
        self.raw_overlay_data = overlay_data
        self.overlay_is_grayscale = is_grayscale

        # Upload to visualiser
        self.visualiser.update_overlay(overlay_reshaped)
        self.visualiser.redraw()

    def _remove_overlay(self) -> None:
        self.visualiser.remove_overlay()
        self.visualiser.redraw()

    def _hide_overlay(self) -> None:
        self.visualiser.hide_overlay()

    def _show_overlay(self) -> None:
        self.visualiser.show_overlay()
