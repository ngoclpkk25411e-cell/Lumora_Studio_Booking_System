from PyQt6.QtWidgets import QApplication, QMainWindow
import sys

from guest_ui.home.ui.HomeMainWindowEx import HomeMainWindowEx


if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWindow = QMainWindow()   # ✅ giữ reference
    gui = HomeMainWindowEx()
    gui.setupUi(mainWindow)

    mainWindow.show()            # ✅ show window thật

    sys.exit(app.exec())