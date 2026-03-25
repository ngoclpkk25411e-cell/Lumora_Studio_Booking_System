import os
from PyQt6.QtWidgets import QMessageBox, QLineEdit, QMainWindow
from PyQt6.QtGui import QPixmap

from admin_ui.login.ui.LoginMainWindow import Ui_LoginMainWindow


# =========================
# PATH HÌNH ẢNH
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "images")

ICON_USER = os.path.join(IMAGE_DIR, "ic_1.png")
ICON_LOCK = os.path.join(IMAGE_DIR, "ic_2.png")
ICON_LOGIN = os.path.join(IMAGE_DIR, "ic_login.png")
ICON_SHINING = os.path.join(IMAGE_DIR, "ic_shining.png")
ICON_STAR = os.path.join(IMAGE_DIR, "ic_star.png")
ICON_SUBJECT = os.path.join(IMAGE_DIR, "Subject.png")
ICON_THUMBNAIL = os.path.join(IMAGE_DIR, "thumnail.png")


class LoginMainWindowEx(QMainWindow, Ui_LoginMainWindow):

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        # ⭐ LOAD FULL IMAGE
        self.setImages()

        self.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Password)

        self.pushButtonLogin.clicked.connect(self.process_login)
        self.pushButtonBack.clicked.connect(self.goBackHome)

    # =========================
    # SET IMAGES FULL
    # =========================
    def setImages(self):

        # SUBJECT (nếu có)
        try:
            self.labelSubject.setPixmap(QPixmap(ICON_SUBJECT))
        except:
            pass

        # LOGIN ICON
        try:
            self.pushButtonLogin.setPixmap(QPixmap(ICON_LOGIN))
        except:
            pass

        # USER ICON
        try:
            self.labelUser.setPixmap(QPixmap(ICON_USER))
        except:
            pass

        # PASSWORD ICON
        try:
            self.labelLock.setPixmap(QPixmap(ICON_LOCK))
        except:
            pass

        # STAR
        try:
            self.labelStar.setPixmap(QPixmap(ICON_STAR))
        except:
            pass

        # SHINING
        try:
            self.labelShining.setPixmap(QPixmap(ICON_SHINING))
        except:
            pass

        # BACKGROUND IMAGE (thumbnail)
        try:
            self.labelThumbnail.setPixmap(QPixmap(ICON_THUMBNAIL))
        except:
            pass

    # =========================
    # LOGIN
    # =========================
    def process_login(self):

        username = self.lineEditUser.text()
        password = self.lineEditPassword.text()

        if username == "hellolumora@gmail.com" and password == "123456":
            QMessageBox.information(self, "Success", "Login successful!")

            from admin_ui.home_admin.ui.AdminHomeMainWindowEx import AdminHomeMainWindowEx

            self.adminHome = AdminHomeMainWindowEx()
            self.adminHome.show()
            self.close()

        else:
            QMessageBox.warning(self, "Error", "Invalid username or password!")

    def goBackHome(self):
        from guest_ui.home.ui.HomeMainWindowEx import HomeMainWindowEx
        self.homeWindow = HomeMainWindowEx()
        self.homeWindow.show()
        self.close()