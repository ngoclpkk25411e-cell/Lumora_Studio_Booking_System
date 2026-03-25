import os

from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QPixmap   # ⭐ THÊM

from guest_ui.contact.ui.ContactMainWindow import Ui_MainWindow


# =========================
# PATH HÌNH ẢNH
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "images")

ICON_STUDIO = os.path.join(IMAGE_DIR, "Subject 2.png")
IMAGE_STUDIO = os.path.join(IMAGE_DIR, "z7605085109820_e3dcea44fddb87bde9dcd59df6f2434b.jpg")

ICON_PHONE = os.path.join(IMAGE_DIR, "phone-call.png")
ICON_EMAIL = os.path.join(IMAGE_DIR, "email.png")
ICON_LOCATION = os.path.join(IMAGE_DIR, "gps.png")
ICON_CLOCK = os.path.join(IMAGE_DIR, "clock.png")
ICON_BACK = os.path.join(IMAGE_DIR, "left_arrow.png")


class ContactMainWindowEx(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        # ⭐ FIX IMAGE
        self.setImages()

        self.pushButtonBack.clicked.connect(self.goHome)

    # =========================
    # SET IMAGES
    # =========================
    def setImages(self):

        try:
            self.labelLogo.setPixmap(QPixmap(ICON_STUDIO))
        except:
            pass

        try:
            self.labelStudio.setPixmap(QPixmap(IMAGE_STUDIO))
        except:
            pass

        try:
            self.labelPhone.setPixmap(QPixmap(ICON_PHONE))
        except:
            pass

        try:
            self.labelMail.setPixmap(QPixmap(ICON_EMAIL))
        except:
            pass

        try:
            self.labelAddress.setPixmap(QPixmap(ICON_LOCATION))
        except:
            pass

        try:
            self.labelWorking.setPixmap(QPixmap(ICON_CLOCK))
        except:
            pass

        try:
            self.pushButtonBack.setPixmap(QPixmap(ICON_BACK))
        except:
            pass

    # =========================
    # GO HOME
    # =========================
    def goHome(self):

        from guest_ui.home.ui.HomeMainWindowEx import HomeMainWindowEx

        self.home = HomeMainWindowEx()

        self.home.show()

        self.close()