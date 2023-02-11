import sys


from PIL import Image
from PyQt5.QtCore import Qt
from ui import Ui_MainWindow
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

import api

# FALLBACK_MAP = Image.open("/".join(__file__.split("/")[:-1]) + "/fallback.png")
FALLBACK_MAP = Image.open("loading.png")
ZOOM_BOUNDS = 0, 17


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        self.search_line.returnPressed.connect(self.draw_map)

        self.height_offset = self.clear_search.height() + self.hybrid.height()
        self.zoom = api.DEFAULT_ZOOM
        self.step = api.DEFAULT_STEP
        self.current_coords = list(api.DEFAULT_LOCATION)
        self.last_map = None

        self.map.move(0, self.height_offset)
        self.resize(api.MAP_SIZE[0], api.MAP_SIZE[1] + self.height_offset)

        self.draw_map()

    def draw_map(self, dx=0, dy=0):
        try:
            coords = list(api.locate(self.search_line.text()))
            self.current_coords[0] += dx
            self.current_coords[1] += dy
            if not coords:
                coords = self.current_coords
            map = api.get_map(coords, zoom=self.zoom)
        except api.ApiException:
            if self.last_map:
                map = self.last_map
            else:
                map = FALLBACK_MAP

        self.map.setPixmap(QPixmap.fromImage(convert_image_to_qimage(map)))

        self.last_map = map

    def keyPressEvent(self, event):
        dx, dy = 0, 0
        if (key := event.key()) in {Qt.Key_PageUp, Qt.Key_PageDown, Qt.Key_Up, Qt.Key_Down, Qt.Key_Right,
                                    Qt.Key_Left}:
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

            self.draw_map(dx=dx, dy=dy)


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
