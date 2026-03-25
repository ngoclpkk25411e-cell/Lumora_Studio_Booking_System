import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from guest_ui.review.ui.ReviewMainWindowEx import ReviewMainWindowEx

app = QApplication(sys.argv)

window = QMainWindow()
ui = ReviewMainWindowEx()
ui.setupUi(window)

window.show()

app.exec()