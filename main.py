import sys

from ui import Ui_MainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from math import ceil

from api import Scheme, get_map


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        self.height_offset = self.clear_search.height() + self.hybrid.height()
        self.longitude = -25.694422
        self.latitude = 133.791467
        self.spn = [25, 35]
        self.scheme = Scheme.Map
        self.draw_map()

    def draw_map(self):
        self.pixmap = QPixmap.fromImage(
            get_map(self.longitude, self.latitude, self.spn, scheme=self.scheme)
        )

        self.map.move(0, self.height_offset)
        self.map.setPixmap(self.pixmap)

        self.resize(self.map.width(), self.map.height() + self.height_offset)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageUp:
            self.spn = (round(self.spn[0] / 1.1, 2), round(self.spn[1] / 1.1, 2))
        elif event.key() == Qt.Key_PageDown:
            self.spn = (ceil(self.spn[0] * 1.1), ceil(self.spn[1] * 1.1))
        print(self.spn)
        self.draw_map()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
