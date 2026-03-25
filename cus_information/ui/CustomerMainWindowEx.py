import json
import os
from collections import Counter

from PyQt6.QtWidgets import QWidget, QListWidgetItem, QTableWidgetItem, QMessageBox
from PyQt6.QtGui import QColor, QPixmap, QFont
from PyQt6.QtCore import Qt

from .CustomerMainWindow import Ui_Form
from Lumora_Studio_Booking_System.utils_path import resource_path, ensure_data_file


class CustomerMainWindowEx(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # bookings.json phải dùng file dữ liệu thật bên ngoài exe
        self.booking_path = ensure_data_file("datasets/bookings.json")

        # avatar chỉ đọc ảnh bundle
        self.avatar_path = resource_path("admin_ui/home_admin/images/user.png")

        self.bookings = []
        self.customers = {}

        self.applyModernStyle()
        self.loadBookings()
        self.loadCustomerList()
        self.loadAvatar()

        self.listWidgetCustomers.itemClicked.connect(self.showCustomerDetail)
        self.lineEditSearch.textChanged.connect(self.searchCustomer)
        self.pushButtonBack.clicked.connect(self.goBack)

        if hasattr(self, "pushButtonStatistics"):
            self.pushButtonStatistics.clicked.connect(self.showStatistics)

        self.tableWidgetBooking.horizontalHeader().setStretchLastSection(True)

    def applyModernStyle(self):
        self.setStyleSheet("""
        QWidget {
            background-color: #F7F1EA;
            color: #6B3F1D;
            font-family: "Times New Roman";
            font-size: 14px;
        }

        QLabel {
            color: #6B3F1D;
            background: transparent;
            border: none;
        }

        QPushButton {
            background-color: #F3E7D8;
            color: #7A4A22;
            border: 1.5px solid #A97B50;
            border-radius: 18px;
            padding: 8px 14px;
            font-size: 15px;
            font-weight: 700;
        }

        QPushButton:hover {
            background-color: #EAD9C5;
        }

        QPushButton:pressed {
            background-color: #DFC9B1;
        }

        QLineEdit {
            background-color: #FFF9F3;
            color: #6B3F1D;
            border: 1.5px solid #C69C72;
            border-radius: 12px;
            padding: 8px 10px;
            font-size: 14px;
            selection-background-color: #D8B48A;
            selection-color: #FFFFFF;
        }

        QListWidget {
            background-color: #FFF9F3;
            color: #6B3F1D;
            border: 1.5px solid #C69C72;
            border-radius: 12px;
            padding: 6px;
            font-size: 14px;
            outline: 0;
        }

        QListWidget::item {
            background-color: transparent;
            color: #6B3F1D;
            border-radius: 10px;
            padding: 10px 12px;
            margin: 4px 0px;
        }

        QListWidget::item:selected {
            background-color: #B78B60;
            color: white;
            border: 1px solid #8B5A2B;
        }

        QListWidget::item:hover {
            background-color: #F0E0CD;
        }

        QTableWidget {
            background-color: #FFF9F3;
            color: #6B3F1D;
            gridline-color: #D8C1A8;
            border: 1.5px solid #C69C72;
            border-radius: 12px;
            font-size: 14px;
        }

        QHeaderView::section {
            background-color: #E9D6BF;
            color: #6B3F1D;
            border: none;
            border-bottom: 1px solid #C69C72;
            padding: 10px;
            font-size: 14px;
            font-weight: 700;
        }

        QTableWidget::item {
            padding: 8px;
        }

        QScrollBar:vertical {
            background: #F3E7D8;
            width: 12px;
            margin: 0px;
            border-radius: 6px;
        }

        QScrollBar::handle:vertical {
            background: #C69C72;
            min-height: 30px;
            border-radius: 6px;
        }

        QScrollBar:horizontal {
            background: #F3E7D8;
            height: 12px;
            margin: 0px;
            border-radius: 6px;
        }

        QScrollBar::handle:horizontal {
            background: #C69C72;
            min-width: 30px;
            border-radius: 6px;
        }
        """)

        if hasattr(self, "pushButtonBack"):
            self.pushButtonBack.setText("Back")
            self.pushButtonBack.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: black;
                border: none;
                font-family: "Times New Roman";
                font-size: 15px;
                font-weight: 700;
                padding: 6px 18px;
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

        for widget in [
            getattr(self, "lineEditName", None),
            getattr(self, "lineEditPhone", None),
            getattr(self, "lineEditEmail", None),
            getattr(self, "lineEditSearch", None),
        ]:
            if widget is not None:
                widget.setFont(QFont("Times New Roman", 14))

        title_candidates = [
            "labelTitle", "labelHeader", "labelCustomerInfo",
            "label_2", "label_3", "label_4"
        ]
        for name in title_candidates:
            if hasattr(self, name):
                lb = getattr(self, name)
                if lb and hasattr(lb, "text"):
                    txt = lb.text().lower()
                    if "customer" in txt:
                        lb.setStyleSheet("""
                        QLabel {
                            background: transparent;
                            color: #6B3F1D;
                            border: none;
                            font-family: "Times New Roman";
                            font-size: 28px;
                            font-weight: 700;
                        }
                        """)
                        lb.setMinimumHeight(50)

        if hasattr(self, "labelAvatar"):
            self.labelAvatar.setStyleSheet("""
            QLabel {
                background-color: #F8F8F8;
                border: 2px solid #C69C72;
                border-radius: 12px;
            }
            """)

    def loadAvatar(self):
        if os.path.exists(self.avatar_path):
            pix = QPixmap(self.avatar_path)
            pix = pix.scaled(
                90,
                90,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            if hasattr(self, "labelAvatar"):
                self.labelAvatar.setPixmap(pix)
                self.labelAvatar.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def loadBookings(self):
        if os.path.exists(self.booking_path):
            with open(self.booking_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if isinstance(data, list):
                self.bookings = data
            else:
                self.bookings = data.get("bookings", [])
        else:
            self.bookings = []

    def loadCustomerList(self):
        self.customers.clear()
        self.listWidgetCustomers.clear()

        for booking in self.bookings:
            name = booking.get("name", "")
            email = booking.get("email", "")
            phone = booking.get("phone", "")

            customer_key = f"{name}|{email}"

            if customer_key not in self.customers:
                self.customers[customer_key] = {
                    "name": name,
                    "phone": phone,
                    "email": email,
                    "bookings": []
                }

            self.customers[customer_key]["bookings"].append(booking)

        for key in self.customers:
            name = self.customers[key]["name"]
            email = self.customers[key]["email"]

            text = f"{name} ({email})"

            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, key)
            self.listWidgetCustomers.addItem(item)

    def searchCustomer(self):
        keyword = self.lineEditSearch.text().lower()
        self.listWidgetCustomers.clear()

        for key in self.customers:
            name = self.customers[key]["name"]
            email = self.customers[key]["email"]
            text = f"{name} ({email})"

            if keyword in text.lower():
                item = QListWidgetItem(text)
                item.setData(Qt.ItemDataRole.UserRole, key)
                self.listWidgetCustomers.addItem(item)

    def showCustomerDetail(self, item):
        key = item.data(Qt.ItemDataRole.UserRole)
        customer = self.customers[key]

        self.lineEditName.setText(customer["name"])
        self.lineEditPhone.setText(customer["phone"])
        self.lineEditEmail.setText(customer["email"])

        self.loadBookingHistory(customer["bookings"])

    def loadBookingHistory(self, bookings):
        self.tableWidgetBooking.clearContents()
        self.tableWidgetBooking.setRowCount(len(bookings))

        for row, booking in enumerate(bookings):
            date_item = QTableWidgetItem(str(booking.get("date", "")))
            qty_item = QTableWidgetItem(str(booking.get("number_people", "")))
            package_item = QTableWidgetItem(str(booking.get("package", "")))
            concept_item = QTableWidgetItem(str(booking.get("concept", "")))

            for item in [date_item, qty_item, package_item, concept_item]:
                item.setForeground(QColor("#6B3F1D"))

            self.tableWidgetBooking.setItem(row, 0, date_item)
            self.tableWidgetBooking.setItem(row, 1, qty_item)
            self.tableWidgetBooking.setItem(row, 2, package_item)
            self.tableWidgetBooking.setItem(row, 3, concept_item)

            status = booking.get("status", "Pending")
            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

            if status.lower() == "confirmed":
                status_item.setBackground(QColor("#C8E6C9"))
                status_item.setForeground(QColor("#1B5E20"))
            elif status.lower() == "pending":
                status_item.setBackground(QColor("#FFE0B2"))
                status_item.setForeground(QColor("#E65100"))
            elif status.lower() == "cancelled":
                status_item.setBackground(QColor("#FFCDD2"))
                status_item.setForeground(QColor("#B71C1C"))
            else:
                status_item.setForeground(QColor("#6B3F1D"))

            self.tableWidgetBooking.setItem(row, 4, status_item)

        self.tableWidgetBooking.resizeRowsToContents()

    def showStatistics(self):
        selected = self.listWidgetCustomers.currentItem()

        if not selected:
            QMessageBox.warning(self, "Warning", "Please select a customer first.")
            return

        key = selected.data(Qt.ItemDataRole.UserRole)
        customer = self.customers[key]
        bookings = customer["bookings"]

        total_bookings = len(bookings)
        dates = [b.get("date", "") for b in bookings if b.get("date", "")]
        first_booking = min(dates) if dates else ""
        last_booking = max(dates) if dates else ""
        concepts = [b.get("concept", "") for b in bookings if b.get("concept", "")]
        most_common = Counter(concepts).most_common(1)[0][0] if concepts else ""

        message = f"""
Customer Statistics

Customer: {customer["name"]}

Total bookings: {total_bookings}

First booking: {first_booking}
Last booking: {last_booking}

Most booked concept: {most_common}
"""
        QMessageBox.information(self, "Statistics", message)

    def goBack(self):
        from Lumora_Studio_Booking_System.admin_ui.home_admin.ui.AdminHomeMainWindowEx import AdminHomeMainWindowEx

        self.adminHome = AdminHomeMainWindowEx()
        self.adminHome.show()
        self.close()