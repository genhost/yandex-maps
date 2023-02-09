from ui import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QPixmap


from api import Scheme, get_map


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        super().setupUi(self)
        height_offset = self.clear_search.height() + self.hybrid.height()
        print((self.width(), self.height() - height_offset))
        self.pixmap = QPixmap.fromImage(get_map(-25.694422, 133.791467,
                                                scheme=Scheme.Map))

        self.map.move(0, height_offset)
        self.map.setPixmap(self.pixmap)
        self.resize(self.map.width(), self.map.height() + height_offset)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
