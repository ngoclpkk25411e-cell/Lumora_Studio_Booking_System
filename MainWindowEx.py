from Do_an.Home.MainWindow import Ui_Home


class MainWindowEx(Ui_Home):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
    def showWindow(self):
        self.MainWindow.show()