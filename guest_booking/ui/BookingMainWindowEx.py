import os

from PyQt6.QtWidgets import QMainWindow, QMessageBox

from guest_ui.guest_booking.models.booking import Booking
from guest_ui.guest_booking.ui.BookingMainWindow import Ui_MainWindow


# =========================
# PATH HÌNH ẢNH (THÊM MỚI)
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "..", "images")

ICON_LOGO = os.path.join(IMAGE_DIR, "Subject 2.png")
ICON_CAMERA = os.path.join(IMAGE_DIR, "camera.png")


class BookingMainWindowEx(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.setupCombobox()
        self.setupSignal()

        self.pushButtonBack.clicked.connect(self.goHome)

    # =========================
    # GO HOME
    # =========================
    def goHome(self):

        from guest_ui.home.ui.HomeMainWindowEx import HomeMainWindowEx

        self.home = HomeMainWindowEx()
        self.home.show()

        self.close()

    # =========================
    # SETUP COMBOBOX
    # =========================
    def setupCombobox(self):

        self.comboBoxSessionPackage.clear()
        self.comboBoxSessionPackage.addItems([
            "Individual",
            "Couple",
            "Family",
            "Group"
        ])

        self.comboBoxConcept.clear()
        self.comboBoxConcept.addItems([
            "Profile / CV / LinkedIn",
            "Portrait",
            "Birthday",
            "Generation Concept",
            "Pre-wedding Basic"
        ])

        self.comboBoxLocation.clear()
        self.comboBoxLocation.addItems([
            "Studio Light",
            "Outdoor / Nature",
        ])

        self.comboBoxNum.clear()
        self.comboBoxNum.addItems([
            "1", "2", "3", "4", "5", "6", "7",
            "More (please specify in notes)"
        ])

    # =========================
    # SIGNAL
    # =========================
    def setupSignal(self):
        self.btnBook.clicked.connect(self.process_book)

    # =========================
    # BOOK BUTTON
    # =========================
    def process_book(self):

        name = self.lineEditFullName.text().strip()
        email = self.lineEditEmail.text().strip()
        phone = self.lineEditPhoneNum.text().strip()

        # VALIDATION
        if name == "":
            QMessageBox.warning(self, "Warning", "Please enter your name")
            return

        if email == "":
            QMessageBox.warning(self, "Warning", "Please enter your email")
            return

        # DATE + TIME
        date = self.dateEdit.date().toString("yyyy-MM-dd")
        time = self.timeEdit.time().toString("HH:mm")

        concept = self.comboBoxConcept.currentText()
        location = self.comboBoxLocation.currentText()
        number_people = self.comboBoxNum.currentText()
        package = self.comboBoxSessionPackage.currentText()

        notes = self.textEditNotes.toPlainText().strip()
        promo = self.lineEditCode.text().strip()

        booking = Booking(
            None,
            name,
            email,
            phone,
            date,
            time,
            concept,
            location,
            number_people,
            package,
            notes,
            promo
        )

        from guest_ui.after_booking.ui.AfterBookingMainWindowEx import AfterBookingMainWindowEx

        self.afterWindow = AfterBookingMainWindowEx(booking)

        self.afterWindow.show()

        self.close()

    # =========================
    # CLEAR FORM
    # =========================
    def clearForm(self):

        self.lineEditFullName.clear()
        self.lineEditEmail.clear()
        self.lineEditPhoneNum.clear()
        self.textEditNotes.clear()
        self.lineEditCode.clear()

        self.comboBoxConcept.setCurrentIndex(0)
        self.comboBoxLocation.setCurrentIndex(0)
        self.comboBoxNum.setCurrentIndex(0)
        self.comboBoxSessionPackage.setCurrentIndex(0)