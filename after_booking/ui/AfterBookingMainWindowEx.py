import os
import sys

from PyQt6.QtWidgets import QMainWindow, QMessageBox, QLabel, QTextEdit
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from .AfterBookingMainWindow import Ui_MainWindow
from ...guest_booking.models.bookings import Bookings


def resource_path(relative_path: str) -> str:
    """
    Lấy đường dẫn file dùng được cả khi chạy bình thường lẫn khi đóng gói exe.
    """
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    # project root: Lumora_Studio_Booking_System
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
    return os.path.join(base_path, relative_path)


def writable_data_path(relative_path: str) -> str:
    """
    Đường dẫn dữ liệu ghi được sau khi đóng gói.
    Không nên ghi file JSON vào _MEIPASS vì đó là thư mục tạm/read-only.
    """
    if getattr(sys, "frozen", False):
        base_dir = os.path.dirname(sys.executable)
    else:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))

    full_path = os.path.join(base_dir, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    return full_path


class AfterBookingMainWindowEx(QMainWindow, Ui_MainWindow):
    def __init__(self, booking):
        super().__init__()
        self.setupUi(self)
        self.label_6.setStyleSheet("""
        QLabel {
            border: none;
            background: transparent;
            color: #8a5628;
            font-size: 34px;
            font-weight: bold;
        }
        """)

        parent = self.label_6.parentWidget()
        if parent:
            parent.setStyleSheet("""
            QFrame {
                border: none;
                background: transparent;
            }
            """)

        self.booking = booking
        self.home = None
        self.bookingWindow = None

        self.setupUiStyle()
        self.setupImages()
        self.showBookingInfo()

        self.pushButtonConfirm.clicked.connect(self.confirmBooking)
        self.pushButtonEdit.clicked.connect(self.editBooking)

    def setupUiStyle(self):
        self.setStyleSheet("""
        QMainWindow, QWidget {
            background-color: #f6efe7;
            color: #8a5628;
            font-family: "Times New Roman";
        }

        QLabel {
            color: #8a5628;
        }

        QTextEdit {
            background-color: #f8f1e9;
            border: 1px solid #d8c7b6;
            border-radius: 10px;
            padding: 8px;
            font-size: 13px;
            color: #7a4b22;
        }

        QPushButton {
            background-color: #c79660;
            color: white;
            border: none;
            border-radius: 12px;
            padding: 8px 18px;
            font-size: 13px;
            font-weight: bold;
        }

        QPushButton:hover {
            background-color: #b6844d;
        }
        """)

        if hasattr(self, "textEditAppointment") and isinstance(self.textEditAppointment, QTextEdit):
            self.textEditAppointment.setReadOnly(True)
            self.textEditAppointment.setStyleSheet("""
                QTextEdit {
                    background-color: #f8f1e9;
                    border: 1px solid #d8c7b6;
                    border-radius: 10px;
                    padding: 10px;
                    font-size: 12px;
                    line-height: 1.35;
                    color: #7a4b22;
                }
            """)

        # thu nhỏ các label to để khỏi bị mất chữ
        for label_name in [
            "labelTitle", "labelHeader", "labelThanks",
            "labelNotificationTitle", "labelStudioName"
        ]:
            label = getattr(self, label_name, None)
            if isinstance(label, QLabel):
                label.setWordWrap(True)
                label.setStyleSheet("""
                    QLabel {
                        color: #8a5628;
                        font-size: 12px;
                        font-weight: bold;
                    }
                """)

        # nếu UI của bạn có đúng objectName theo ảnh thì chỉnh riêng luôn
        for label_name, size in {
            "label_2": 16,
            "label_3": 13,
            "label_4": 12,
            "label_5": 12,
            "label_6": 16,
        }.items():
            label = getattr(self, label_name, None)
            if isinstance(label, QLabel):
                label.setWordWrap(True)
                label.setStyleSheet(f"""
                    QLabel {{
                        color: #8a5628;
                        font-size: {size}px;
                        font-weight: bold;
                    }}
                """)

    def set_pixmap(self, label: QLabel, image_path: str, keep_ratio: bool = True):
        if not label or not os.path.exists(image_path):
            return

        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            return

        w = max(label.width(), 60)
        h = max(label.height(), 60)

        if keep_ratio:
            pixmap = pixmap.scaled(
                w, h,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        else:
            pixmap = pixmap.scaled(
                w, h,
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def setupImages(self):
        # chỉnh path ảnh để chạy được cả IDE lẫn exe
        thank_you_path = resource_path("guest_ui/after_booking/images/thank-you.png")
        logo_path = resource_path("guest_ui/after_booking/images/Subject 2.png")

        # set an toàn, objectName nào không có cũng không crash
        possible_logo_labels = ["labelLogo", "label_logo", "label", "label_7"]
        possible_thank_labels = ["labelThankYou", "label_thankyou", "labelImage", "label_8"]

        for name in possible_logo_labels:
            lb = getattr(self, name, None)
            if isinstance(lb, QLabel):
                self.set_pixmap(lb, logo_path)
                break

        for name in possible_thank_labels:
            lb = getattr(self, name, None)
            if isinstance(lb, QLabel):
                self.set_pixmap(lb, thank_you_path, keep_ratio=False)
                break

    def showBookingInfo(self):
        text = (
            f"Name: {self.booking.name}\n"
            f"Email: {self.booking.email}\n"
            f"Phone: {self.booking.phone}\n\n"
            f"Date: {self.booking.date}\n"
            f"Time: {self.booking.time}\n\n"
            f"Concept: {self.booking.concept}\n"
            f"Location: {self.booking.location}\n\n"
            f"People: {self.booking.number_people}\n"
            f"Package: {self.booking.package}\n\n"
            f"Notes: {self.booking.notes if self.booking.notes else 'None'}\n"
            f"Promo Code: {self.booking.promo if self.booking.promo else 'None'}"
        )

        self.textEditAppointment.setPlainText(text)

    def confirmBooking(self):
        try:
            from Lumora_Studio_Booking_System.utils_path import ensure_data_file
            from ...home.ui.HomeMainWindowEx import HomeMainWindowEx

            bookings = Bookings()
            file_path = ensure_data_file("datasets/bookings.json")

            if os.path.exists(file_path):
                bookings.import_json(file_path)

            self.booking.booking_id = f"B{len(bookings.list) + 1:03d}"
            bookings.add_booking(self.booking)
            bookings.export_json(file_path)

            QMessageBox.information(
                self,
                "Success",
                f"Your appointment has been confirmed!\nBooking ID: {self.booking.booking_id}"
            )

            self.home = HomeMainWindowEx()
            self.home.show()
            self.close()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Cannot confirm booking:\n{e}")

    def editBooking(self):
        try:
            from ...guest_booking.ui.BookingMainWindowEx import BookingMainWindowEx
            self.bookingWindow = BookingMainWindowEx()
            self.bookingWindow.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Cannot open booking form:\n{e}")