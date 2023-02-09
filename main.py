import sys

from ui import Ui_MainWindow
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt
from math import ceil

import api
from api import Scheme


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        self.search_line.returnPressed.connect(self.draw_map)

        self.height_offset = self.clear_search.height() + self.hybrid.height()

    def draw_map(self):
        print("drawn")
        # coords = api.locate(self.search_line.text())
        map = api.get_map(55.7522, 37.6156)

        self.pixmap = QPixmap.fromImage(QImage(ImageQt(map)))

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
