import sys
import os
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

class ContactWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        ui_path = os.path.join(os.path.dirname(__file__), "ContactMainWindow.ui")
        uic.loadUi(ui_path, self)

        self.setWindowTitle("Lumora – Contact Us")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ContactWindow()
    win.show()
    sys.exit(app.exec())