import os
import sys

from PyQt6.QtWidgets import QMainWindow, QMessageBox
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt

from ..models.booking import Booking
from .BookingMainWindow import Ui_MainWindow


def resource_path(relative_path: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)

    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
    return os.path.join(base_path, relative_path)


class BookingMainWindowEx(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setupBackButtonStyle()
        self.setupImages()
        self.setupTextFix()
        self.setupCombobox()
        self.setupSignal()

        self.pushButtonBack.clicked.connect(self.goHome)

    def setupBackButtonStyle(self):
        self.pushButtonBack.setText("Back")
        self.pushButtonBack.setIcon(QIcon())
        self.pushButtonBack.setMinimumSize(90, 34)
        self.pushButtonBack.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            color: black;
            border: none;
            border-radius: 0px;
            font-size: 15px;
            padding: 6px 18px;
            text-align: center;
        }
        QPushButton:hover {
            background-color: #e8dcc8;
            color: black;
            border: none;
        }
        QPushButton:pressed {
            background-color: #d9c8ad;
            color: black;
            border: none;
        }
        """)

    def set_label_image(self, label, image_path, keep_ratio=True):
        if label is None or not os.path.exists(image_path):
            return

        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            return

        if keep_ratio:
            scaled = pixmap.scaled(
                label.width(),
                label.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            label.setPixmap(scaled)
            label.setScaledContents(False)
        else:
            label.setPixmap(pixmap)
            label.setScaledContents(True)

        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def setupImages(self):
        logo_path = resource_path("guest_ui/guest_booking/images/Subject 2.png")
        deco_path = resource_path("guest_ui/guest_booking/images/ChatGPT Image Feb 13, 2026, 11_20_27 PM.png")

        # Logo: objectName đúng là labelLogo
        if hasattr(self, "labelLogo") and self.labelLogo and os.path.exists(logo_path):
            self.labelLogo.setMinimumSize(65, 65)
            self.labelLogo.setStyleSheet("background: transparent;")
            self.set_label_image(self.labelLogo, logo_path, keep_ratio=True)

        # Ảnh trang trí bên phải: objectName đúng là label_14
        if hasattr(self, "label_14") and self.label_14 and os.path.exists(deco_path):
            self.label_14.setStyleSheet("background: transparent;")
            self.set_label_image(self.label_14, deco_path, keep_ratio=True)

    def setupTextFix(self):
        # labelDesc đã cao 60 nên chỉ cần wrap cho chắc
        if hasattr(self, "labelDesc") and self.labelDesc:
            self.labelDesc.setWordWrap(True)

        # Dòng cảm ơn cuối: objectName đúng là label_15
        if hasattr(self, "label_15") and self.label_15:
            self.label_15.setWordWrap(False)
            self.label_15.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.label_15.setGeometry(250, 570, 800, 35)
            self.label_15.setStyleSheet("""
            QLabel#label_15 {
                color: #8b6b52;
                font-family: "Playfair Display";
                font-size: 10px;
                background-color: transparent;
                border: none;
            }
            """)

    def goHome(self):
        from Lumora_Studio_Booking_System.guest_ui.home.ui.HomeMainWindowEx import HomeMainWindowEx

        self.home = HomeMainWindowEx()
        self.home.show()
        self.close()

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

    def setupSignal(self):
        self.btnBook.clicked.connect(self.process_book)

    def process_book(self):
        name = self.lineEditFullName.text().strip()
        email = self.lineEditEmail.text().strip()
        phone = self.lineEditPhoneNum.text().strip()

        if name == "":
            QMessageBox.warning(self, "Warning", "Please enter your name")
            return

        if email == "":
            QMessageBox.warning(self, "Warning", "Please enter your email")
            return

        date = self.dateEdit.date().toString("yyyy-MM-dd")
        time = self.timeEdit.time().toString("HH:mm")

        concept = self.comboBoxConcept.currentText()
        location = self.comboBoxLocation.currentText()
        number_people = self.comboBoxNum.currentText()
        package_name = self.comboBoxSessionPackage.currentText()

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
            package_name,
            notes,
            promo
        )

        from Lumora_Studio_Booking_System.guest_ui.after_booking.ui.AfterBookingMainWindowEx import AfterBookingMainWindowEx

        self.afterWindow = AfterBookingMainWindowEx(booking)
        self.afterWindow.show()
        self.close()

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