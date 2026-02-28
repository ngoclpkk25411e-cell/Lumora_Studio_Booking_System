from PyQt6.QtWidgets import QMainWindow


from Do_an.Contact.ui.ContactMainWindowEx import ContactMainWindowEx
from Do_an.Gallery.ui.GalleryMainWindowEx import GalleryMainWindowEx
from Do_an.Home.MainWindow import Ui_Home
from Do_an.Review.ReviewMainWindowEx import ReviewMainWindowEx
from Do_an.Booking.ui.MainWindowEx import MainWindowEx as BookingWindowEx

class MainWindowEx(Ui_Home):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.setupSignalAndSlot()
    def showWindow(self):
        self.MainWindow.show()

    def setupSignalAndSlot(self):
        self.btnGallery_2.clicked.connect(self.openReview)
        self.btnContact.clicked.connect(self.openContact)
        self.btnGallery.clicked.connect(self.openGallery)
        self.btnBooking.clicked.connect(self.openBooking)

    def openReview(self):
        self.reviewWindow = QMainWindow()
        self.uiReview = ReviewMainWindowEx()
        self.uiReview.setupUi(self.reviewWindow)

        self.reviewWindow.show()

        self.MainWindow.close()

    def openContact(self):
        self.contactWindow = QMainWindow()
        self.uiContact = ContactMainWindowEx()
        self.uiContact.setupUi(self.contactWindow)

        self.contactWindow.show()
        self.MainWindow.close()

    def openGallery(self):
        self.galleryWindow = QMainWindow()
        self.uiGallery = GalleryMainWindowEx()
        self.uiGallery.setupUi(self.galleryWindow)

        self.galleryWindow.show()
        self.MainWindow.close()

    def openBooking(self):
        self.bookingWindow = QMainWindow()
        self.uiBooking = BookingWindowEx()
        self.uiBooking.setupUi(self.bookingWindow)

        self.bookingWindow.show()
        self.MainWindow.close()