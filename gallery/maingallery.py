import sys
import os
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

class GalleryWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(__file__), "MainWindow.ui")
        uic.loadUi(ui_path, self)

        self.setWindowTitle("Lumora – Gallery")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = GalleryWindow()
    win.show()
    sys.exit(app.exec())