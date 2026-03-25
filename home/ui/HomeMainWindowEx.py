import os
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QPixmap

# UI
from guest_ui.home.ui.HomeMainWindow import Ui_Home

# NAVIGATION
from guest_ui.contact.ui.ContactMainWindowEx import ContactMainWindowEx
from guest_ui.guest_booking.ui.BookingMainWindowEx import BookingMainWindowEx
from guest_ui.guest_gallery.ui.GuestGalleryMainWindowEx import GuestGalleryMainWindowEx
from guest_ui.review.ui.ReviewMainWindowEx import ReviewMainWindowEx
from admin_ui.login.ui.LoginMainWindowEx import LoginMainWindowEx   # ⭐ NEW


# =========================
# PATH HÌNH ẢNH
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "images")

SUBJECT_IMAGE = os.path.join(IMAGE_DIR, "Subject 2.png")
THUMBNAIL_IMAGE = os.path.join(IMAGE_DIR, "thumnail.jpg")


class HomeMainWindowEx(QMainWindow, Ui_Home):

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        # Load ảnh
        self.setImages()

        # Setup signal
        self.setupSignalAndSlot()

    # =========================
    # SET IMAGES
    # =========================
    def setImages(self):

        if os.path.exists(SUBJECT_IMAGE):
            try:
                self.label_4.setPixmap(QPixmap(SUBJECT_IMAGE))
            except:
                pass

        if os.path.exists(THUMBNAIL_IMAGE):
            try:
                self.label.setPixmap(QPixmap(THUMBNAIL_IMAGE))
            except:
                pass

    # =========================
    # SIGNAL
    # =========================
    def setupSignalAndSlot(self):

        # MENU
        self.btnReview.clicked.connect(self.openReview)
        self.btnContact.clicked.connect(self.openContact)
        self.btnGallery.clicked.connect(self.openGallery)

        # BUTTON
        self.btnBooking.clicked.connect(self.openBooking)

        # ⭐ LOGIN BUTTON (NEW)
        self.pushButtonLogin.clicked.connect(self.openLogin)

    # =========================
    # NAVIGATION
    # =========================
    def openReview(self):
        self.reviewWindow = ReviewMainWindowEx()
        self.reviewWindow.show()
        self.close()

    def openContact(self):
        self.contactWindow = ContactMainWindowEx()
        self.contactWindow.show()
        self.close()

    def openGallery(self):
        self.galleryWindow = GuestGalleryMainWindowEx()
        self.galleryWindow.show()
        self.close()

    def openBooking(self):
        self.bookingWindow = BookingMainWindowEx()
        self.bookingWindow.show()
        self.close()

    # ⭐ LOGIN
    def openLogin(self):
        self.loginWindow = LoginMainWindowEx()
        self.loginWindow.show()
        self.close()