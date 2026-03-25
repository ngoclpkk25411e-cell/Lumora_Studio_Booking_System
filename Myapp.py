from PyQt6.QtWidgets import QApplication, QMainWindow

from Do_an.Home.MainWindowEx import MainWindowEx

app=QApplication([])
gui=MainWindowEx()
gui.setupUi(QMainWindow())
gui.showWindow()
app.exec()