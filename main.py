import sys


from math import ceil
from PIL import Image
from PyQt5.QtCore import Qt
from ui import Ui_MainWindow
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

import api

CURRENT_DIR = "/".join(__file__.split("/")[:-1])
# FALLBACK_MAP = Image.open(CURRENT_DIR + "/fallback.png")
FALLBACK_MAP = Image.open(CURRENT_DIR + "/loading.png")
ZOOM_BOUNDS = 0, 17


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        self.search_line.returnPressed.connect(self.draw_map)

        self.height_offset = self.clear_search.height() + self.hybrid.height()
        self.zoom = api.DEFAULT_ZOOM
        self.last_map = None

        self.map.move(0, self.height_offset)
        self.resize(api.MAP_SIZE[0], api.MAP_SIZE[1] + self.height_offset)

        self.draw_map()

    def draw_map(self):
        try:
            coords = api.locate(self.search_line.text())
            map = api.get_map(coords, zoom=self.zoom)
        except api.ApiException:
            if self.last_map:
                map = self.last_map
            else:
                map = FALLBACK_MAP

        self.map.setPixmap(QPixmap.fromImage(convert_image_to_qimage(map)))

        self.last_map = map

    def keyPressEvent(self, event):
        if (key := event.key()) in {Qt.Key_PageUp, Qt.Key_PageDown}:
            if key == Qt.Key_PageUp:
                self.zoom += 1
            elif key == Qt.Key_PageDown:
                self.zoom -= 1

            if self.zoom < ZOOM_BOUNDS[0]:
                self.zoom = ZOOM_BOUNDS[0]
            elif self.zoom > ZOOM_BOUNDS[1]:
                self.zoom = ZOOM_BOUNDS[1]

            self.draw_map()


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
