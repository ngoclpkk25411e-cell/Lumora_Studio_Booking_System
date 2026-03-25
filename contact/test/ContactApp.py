from PyQt6.QtWidgets import QApplication, QMainWindow

from guest_ui.contact.ui.ContactMainWindowEx import ContactMainWindowEx

app=QApplication([])
gui=ContactMainWindowEx()
gui.setupUi(QMainWindow())
gui.show()
app.exec()