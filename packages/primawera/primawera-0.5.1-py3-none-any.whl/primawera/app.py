import sys
from os.path import dirname
from typing import Optional, Union

import numpy as np
from PIL import UnidentifiedImageError
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QAction, QFileDialog, QLabel, \
    QActionGroup, QMessageBox, QMainWindow
from numpy.typing import ArrayLike, NDArray

from primawera import lut
from primawera.html_codes import about_page_content, command_page_content
from primawera.loading import load_data, UnsupportedFormatError
from primawera.modeutils import translate_mode
from primawera.widgets.canvas2d import Canvas2D
from primawera.widgets.canvas3d import Canvas3D
from primawera.widgets.canvascomplex import CanvasComplex


class MainWindow(QtWidgets.QMainWindow):
    """
    The main widget of the Primawera application.
    """
    def __init__(self, filepath: Optional[str] = None,
                 data: Optional[ArrayLike] = None, mode: Optional[str] = None,
                 title: Optional[str] = "Primawera",
                 overlay_data: Optional[NDArray[int]] = None,
                 overlay_is_grayscale: bool = True):
        """
        Constructs the object.

        Parameters
        ----------
        filepath: string, optional
            Path to the image file.
        data: ArrayLike, optional
            Data to visualise. The application will try to readjust it to the
            format (frames, width, height, channels).
        mode: string, optional
            Mode of the image data. Needed if NumPy data is passed in.
        title: string, optional
            Title of the window.
        overlay_data: integer ndarray, optional
            Data to use as overlays. Has to be the same shape as input data.
        overlay_is_grayscale: bool
            Is overlay data grayscale?
        """
        super(MainWindow, self).__init__()
        self.last_accessed_file_path = "."
        self.last_accessed_folder_path = "."

        # First tries to readjust the data to suitable format.
        if data is not None:
            data = np.asanyarray(data)

        if mode is not None:
            mode = mode.strip()
            if filepath is not None:
                QMessageBox \
                    .information(self, "Info",
                                 "Mode was passed alongside path to a file, "
                                 "hence mode will be ignored",
                                 buttons=QMessageBox.Ok,
                                 defaultButton=QMessageBox.Ok)
                mode = None

        if data is not None and mode is not None:
            mode = translate_mode(mode)
            if mode is None:
                QMessageBox \
                    .critical(self, "Error",
                              f"Unrecognized mode '{mode}'!",
                              buttons=QMessageBox.Ok,
                              defaultButton=QMessageBox.Ok)
                raise RuntimeError(
                    f"Provided mode '{mode}' is not recognized.")
            if mode == "rgb" and len(data.shape) == 3:
                data = np.array([data])

        if data is not None and mode is None:
            mode = self._recognize_mode(data)
            if mode is None:
                QMessageBox.critical(self, "Error",
                                     "The mode of the image data "
                                     "could not be automatically "
                                     "decided. Try providing it "
                                     "manually.",
                                     buttons=QMessageBox.Ok,
                                     defaultButton=QMessageBox.Ok)
                raise RuntimeError("The mode of the image data could not be"
                                   "automatically decided.")

        self.setWindowTitle(title)

        # Set up central widget
        self.central_widget = None

        # Set up fonts
        self.main_font = QFont("Noto Sans")
        self.setFont(self.main_font)

        # Set up LUTs
        lut.fill_luts()

        # Get the size of the desktop
        desktop = QApplication.desktop()
        screen_geometry = desktop.screenGeometry(0)
        self.desktop_width = screen_geometry.width()
        self.desktop_height = screen_geometry.height()

        self.canvas = None

        # Create menu
        self._create_actions()
        self._connect_actions()
        self._create_menu_bar()

        # Help window
        self._help_window = None

        # Layout
        try:
            if filepath is not None:
                data, mode = load_data(filepath)
                self._start_visualiser(data, mode, overlay_data,
                                       overlay_is_grayscale)
            elif data is not None:
                assert mode is not None
                self._start_visualiser(data, mode, overlay_data,
                                       overlay_is_grayscale)
            else:
                self.setCentralWidget(QLabel("Please open an image."))
        except UnsupportedFormatError as err:
            self.setCentralWidget(
                QLabel("Error encountered with the following message:\n"
                       f"{err}"))
        except UnidentifiedImageError as err:
            self.setCentralWidget(QLabel(
                f"Error inside PIL library with the following message:\n{err}"
            ))

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_PageDown:
            self.canvas.previous_frame()
        elif event.key() == QtCore.Qt.Key_PageUp:
            self.canvas.next_frame()

    def _recognize_mode(self, array: ArrayLike) -> Optional[str]:
        """If not information about mode is passed, try to recognize it
        automatically."""
        if not isinstance(array, np.ndarray):
            return None
        scalar_type = array.dtype

        if np.issubdtype(scalar_type, np.integer):
            if np.issubdtype(scalar_type, np.bool_):
                return "1"

            # NOTE: this could also be a color image, but the implicit
            #       behaviour is set to "grayscale"
            return "grayscale"
        elif np.issubdtype(scalar_type, np.complex_):
            return "C"
        elif np.issubdtype(scalar_type, np.floating):
            return "F"
        return None

    def _start_visualiser(self, data: ArrayLike, mode: str,
                          overlay_data: Optional[NDArray[int]] = None,
                          overlay_is_grayscale: bool = False) -> None:
        """Starts the visualiser."""
        if self.canvas is not None:
            self.canvas.close()
            self.canvas = None
        if self.central_widget is not None:
            self.central_widget.deleteLater()

        data = np.asanyarray(data)

        if mode == "C":
            # Complex data
            self.canvas = CanvasComplex(data, mode,
                                        self.desktop_height,
                                        self.desktop_width, {}, {})
        elif data.shape[0] == 1:
            # 2D data
            self.canvas = Canvas2D(data, mode, self.desktop_height,
                                   self.desktop_width, {}, {},
                                   overlay_data=overlay_data,
                                   overlay_is_grayscale=overlay_is_grayscale)
        else:
            self.canvas = Canvas3D(data, mode,
                                   self.desktop_height,
                                   self.desktop_width, {},
                                   {}, overlay_data=overlay_data,
                                   overlay_is_grayscale=overlay_is_grayscale)
        self.canvas.menus_changed_signal.connect(self._refresh_menu_bar)

        layout = QtWidgets.QVBoxLayout()
        # NOTE: This is a terrible hack to keep the widget's width to at least
        # 300. For some internal and quite shady reason, if you set the minimum
        # size of the canvas widget directly, the geometry calculations break,
        # causing the whole layout to stop working properly when the user zooms
        # in. Also, for some smart reason, the minimum size of the menubar
        # is completely ignored...
        spacer = QtWidgets.QWidget()
        spacer.setFixedSize(QtCore.QSize(300, 10))
        layout.addWidget(spacer)
        layout.addWidget(self.canvas)
        self.central_widget = QtWidgets.QWidget()
        self.central_widget.setLayout(layout)
        self.setCentralWidget(self.central_widget)
        self._refresh_menu_bar()

    @pyqtSlot()
    def _refresh_menu_bar(self) -> None:
        """Redraws the menu bars."""
        # Clear menubar
        self._create_menu_bar()

        # Update menu with available filters
        menubar = self.menuBar()
        canvas_menus = self.canvas.get_menus()
        for menu_title, actions in canvas_menus:
            # Add the menu
            new_menu = menubar.addMenu(menu_title)

            # Set exclusivity
            action_group = QActionGroup(self)
            for idx, action in enumerate(actions):
                action_group.addAction(action)
                new_menu.addAction(action)
        self._create_menu_bar_post()

    def _create_menu_bar(self) -> None:
        """Creates menu bar."""
        menubar = self.menuBar()
        menubar.clear()

        # File menu
        file_menu = menubar.addMenu("&File")
        file_menu.addAction(self.open_file_action)
        file_menu.addAction(self.open_folder_action)
        file_menu.addAction(self.exit_action)

    def _create_menu_bar_post(self) -> None:
        """Run after the creation of the menu bar. Useful for adding extra
        menus at the right."""
        menubar = self.menuBar()

        # Help menu
        help_menu = menubar.addMenu("&Help")
        help_menu.addAction(self.about_action)
        help_menu.addAction(self.help_commands_action)

    def _create_actions(self) -> None:
        """Create all QActions."""
        self.open_file_action = QAction("Open file...")
        self.open_folder_action = QAction("Open folder...")
        self.exit_action = QAction("Exit")
        self.about_action = QAction("About")
        self.help_commands_action = QAction("Commands")

    def _connect_actions(self) -> None:
        """Connects all actions."""
        self.exit_action.triggered.connect(self.close)
        self.open_file_action.triggered.connect(self.open_file)
        self.open_folder_action.triggered.connect(self.open_folder)
        self.help_commands_action.triggered.connect(self.help_commands)
        self.about_action.triggered.connect(self.about_command)

    def resizeEvent(self, event):
        desktop = QApplication.desktop()
        screen_geometry = desktop.screenGeometry(0)
        self.desktop_width = screen_geometry.width()
        self.desktop_height = screen_geometry.height()
        if self.canvas is not None:
            self.canvas.update_desktop_size(width=self.desktop_width,
                                            height=self.desktop_height)

    def closeEvent(self, event) -> None:
        self.canvas.closeEvent(event)
        if self._help_window is not None:
            self._help_window.close()
        event.accept()

    def open_file(self) -> None:
        """Opens the file selection dialog."""
        file_name, _ = QFileDialog. \
            getOpenFileName(self, "Open file",
                            self.last_accessed_file_path,
                            "Image file (*.jpg *.png"
                            " *.h5 *.tif *.tiff)")
        if file_name == "":
            # User did not select a file
            return

        parent_path = dirname(file_name)  # path to the parent directory
        if file_name != "":
            self.last_accessed_file_path = parent_path

        self._open(file_name)

    def open_folder(self) -> None:
        """Opens the folder selection dialog."""
        folder_name = QFileDialog. \
            getExistingDirectory(self, "Open folder",
                                 self.last_accessed_folder_path,
                                 QFileDialog.ShowDirsOnly
                                 )
        if folder_name == "":
            # No folder was selected
            return
        self.last_accessed_folder_path = folder_name
        self._open(folder_name)

    def _open(self, path: str) -> None:
        """Open a file at given path."""
        try:
            data, mode = load_data(path)
            self._start_visualiser(data, mode)
        except UnsupportedFormatError as err:
            self.setCentralWidget(QLabel(
                "Error inside Primawera encountered with the following "
                f"message:\n{err}"))
        except UnidentifiedImageError as err:
            self.setCentralWidget(QLabel(
                f"Error inside PIL library with the following message:\n{err}"
            ))

    def help_commands(self) -> None:
        """Shows the help window."""
        self._help_window = QLabel(command_page_content)
        self._help_window.setWindowTitle("Primawera - Help window.")
        self._help_window.setFont(self.main_font)
        self._help_window.setMargin(10)
        self._help_window.show()

    def about_command(self) -> None:
        """Shows the 'about' window."""
        self._help_window = QLabel(about_page_content)
        self._help_window.setWindowTitle("Primawera - About window.")
        self._help_window.setFont(self.main_font)
        self._help_window.setMargin(10)
        self._help_window.show()

    def paintEvent(self, event) -> None:
        super().paintEvent(event)
        # NOTE: According to the documentation, the resizeEvent should be
        # called when the window's size changes; however, when the user zooms
        # in, the event is not always called. This function ensures that the
        # new size is calculated properly.
        self.adjustSize()


def print_help(name: str) -> None:
    print(f"Usage: {name} FILEPATH\n"
          f"-----\n"
          f"Filepath specifies path to an image file. It is optional.\n\n")


def run_app(data: Union[str, ArrayLike], mode: Optional[str] = None,
            overlay_data: Optional[NDArray[int]] = None,
            is_overlay_grayscale: bool = True,
            title: str = "Primawera") \
        -> Union[QMainWindow, bool]:
    """
    Creates a Primawera window.

    Parameters
    ----------
    data : string or arraylike object
        Either a path to a file or a numpy array.
    mode : string, optional
        "gray", "color, "rgb", "float" or "complex". Additional aliases
        can be found inside the `modeutils.py` file or inside README.md
    overlay_data : arraylike with integer type, optional
        Data to overlay on top of the image. Can include colours or
        grayscale data, but must have the same dimensions as data.
    is_overlay_grayscale : bool, optional
        Should the overlay data be interpreted as coloured?
    title : string, optional
        The window's title.

    Returns
    -------
    out: bool or MainWindow
        MainWindow object representing the PyQT application or False if
        an error happened.

    """
    app = QtCore.QCoreApplication.instance()
    app_created = False
    if app is None:
        print("Creating app")
        app = QtWidgets.QApplication(sys.argv)
        app_created = True

    if overlay_data is not None:
        if not isinstance(overlay_data, np.ndarray):
            print("Error: Overlay data is not a numpy array! It will be"
                  "ignored.")
            overlay_data = None
        elif len(overlay_data.shape) == 2:
            w, h = overlay_data.shape
            overlay_data = np.reshape(overlay_data, (1, w, h))

    if type(data) == str:
        _window = MainWindow(filepath=data, title=title,
                             overlay_data=overlay_data,
                             overlay_is_grayscale=is_overlay_grayscale)
    elif isinstance(data, np.ndarray):
        if len(data.shape) > 4 or len(data.shape) < 2:
            print(f"Error: Data has invalid shape ({data.shape})!",
                  file=sys.stderr)
            return False
        elif len(data.shape) == 2:
            data = np.array([data])
        _window = MainWindow(data=data, mode=mode, title=title,
                             overlay_data=overlay_data,
                             overlay_is_grayscale=is_overlay_grayscale)
    else:
        print("Error: Invalid input data. Cannot run the app.",
              file=sys.stderr)
        return False
    _window.show()

    if app_created:
        app.exec_()
    return _window


# Inspired by:
# https://cyrille.rossant.net/making-pyqt4-pyside-and-ipython-work-together/
def create_window(filepath: Optional[str] = None):
    """Creates the Primawera window with the passed in file path."""
    app_created = False
    app = QtCore.QCoreApplication.instance()
    if app is None:
        print("Creating app")
        app = QtWidgets.QApplication(sys.argv)
        app_created = True
    app.references = set()
    if filepath is not None:
        _window = MainWindow(filepath=filepath,
                             title=f"Primawera [{filepath}]")
    else:
        _window = MainWindow()
    app.references.add(_window)
    _window.show()

    if app_created:
        app.exec_()
    return _window


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print("Error: Wrong number of arguments!")
        print_help(sys.argv[0])
        exit(1)

    if len(sys.argv) == 2:
        if type(sys.argv[1]) == str and sys.argv[1] == "--help":
            print_help(sys.argv[0])
            exit(0)

        window = create_window(filepath=sys.argv[1])
    else:
        window = create_window()
