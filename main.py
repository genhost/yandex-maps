import sys

from ui import Ui_MainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow

from api import Scheme, get_map


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        super().setupUi(self)

        self.height_offset = self.clear_search.height() + self.hybrid.height()
        self.draw_map()

    def draw_map(self):
        self.pixmap = QPixmap.fromImage(
            get_map(-25.694422, 133.791467, scheme=Scheme.Map)
        )

        self.map.move(0, self.height_offset)
        self.map.setPixmap(self.pixmap)

        self.resize(self.map.width(), self.map.height() + self.height_offset)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
