from PyQt6.QtWidgets import QApplication, QMainWindow

from Lumora_Studio_Booking_System.admin_ui.content.ui.ContentMainWindowEx import ContentMainWindowEx

app=QApplication([])
gui=ContentMainWindowEx()
gui.setupUi(QMainWindow())
gui.show()
app.exec()