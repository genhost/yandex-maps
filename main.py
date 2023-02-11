import sys


from PIL import Image
from PyQt5.QtCore import Qt
from ui import Ui_MainWindow
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

import api
from api import Scheme

CURRENT_DIR = "/".join(__file__.split("/")[:-1])
FALLBACK_MAP = Image.open(CURRENT_DIR + "/data/loading.png")
ZOOM_BOUNDS = 0, 17

HUMAN_SCHEME = {
    "Гибрид": Scheme.Hybrid,
    "Спутник": Scheme.Sattelite,
    "Схема": Scheme.Map,
}


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        self.search_line.returnPressed.connect(self.search)

        self.schematic.toggled.connect(self.update_scheme)
        self.satellite.toggled.connect(self.update_scheme)
        self.hybrid.toggled.connect(self.update_scheme)

        self.height_offset = self.clear_search.height() + self.hybrid.height()

        self.last_map = None
        self.scheme = api.DEFAULT_SCHEME
        self.zoom = api.DEFAULT_ZOOM
        self.step = api.DEFAULT_STEP
        self.coords = api.DEFAULT_LOCATION

        self.map.move(0, self.height_offset)
        self.resize(api.MAP_SIZE[0], api.MAP_SIZE[1] + self.height_offset)

        self.draw_map()

    def draw_map(self):
        try:
            map = api.get_map(self.coords, zoom=self.zoom, scheme=self.scheme)
        except api.ApiException:
            if self.last_map:
                map = self.last_map
            else:
                map = FALLBACK_MAP

        self.map.setPixmap(QPixmap.fromImage(convert_image_to_qimage(map)))

        self.last_map = map

    def update_scheme(self):
        self.unfocus()
        self.scheme = self.current_scheme()
        self.draw_map()

    def search(self):
        self.unfocus()
        try:
            self.coords = api.locate(self.search_line.text())
            self.draw_map()
        except api.ApiException:
            pass

    def shift(self, dx=0, dy=0):
        try:
            self.coords = (
                self.coords[0] + dx,
                self.coords[1] + dy,
            )
            self.draw_map()
        except api.ApiException:
            pass

    def unfocus(self):
        if widget := self.focusWidget():
            widget.clearFocus()

    def keyPressEvent(self, event):
        dx, dy = 0, 0
        key = event.key()

        if key == Qt.Key_Escape:
            self.unfocus()

        if key in {
            Qt.Key_PageUp,
            Qt.Key_PageDown,
            Qt.Key_Up,
            Qt.Key_Down,
            Qt.Key_Right,
            Qt.Key_Left,
        }:
            if key == Qt.Key_PageUp:
                self.zoom += 1
                self.step /= 2
            elif key == Qt.Key_PageDown:
                self.zoom -= 1
                self.step *= 2
            elif key == Qt.Key_Up:
                dy = self.step
            elif key == Qt.Key_Down:
                dy = -self.step
            elif key == Qt.Key_Right:
                dx = self.step
            elif key == Qt.Key_Left:
                dx = -self.step

            if self.zoom < ZOOM_BOUNDS[0]:
                self.zoom = ZOOM_BOUNDS[0]
            elif self.zoom > ZOOM_BOUNDS[1]:
                self.zoom = ZOOM_BOUNDS[1]

            self.shift(dx, dy)

    def current_scheme(self) -> Scheme:
        name = self.scheme_tips.checkedButton().text()
        return HUMAN_SCHEME[name]


def convert_image_to_qimage(image):
    return QImage(
        image.convert("RGBA").tobytes("raw", "BGRA"),
        image.width,
        image.height,
        QImage.Format_ARGB32,
    )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
