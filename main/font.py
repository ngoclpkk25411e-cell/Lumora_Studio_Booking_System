from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QFont
from PyQt6 import uic
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ContactMainWindow.ui", self)
        self.label.setFont(QFont("Playfair Display", 36))

app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(app.exec())
