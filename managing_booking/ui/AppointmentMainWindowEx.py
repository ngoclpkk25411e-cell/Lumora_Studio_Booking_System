import json
import os
from datetime import datetime

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox

from Lumora_Studio_Booking_System.admin_ui.managing_booking.ui.AppointmentMainWindow import Ui_MainWindow
from Lumora_Studio_Booking_System.utils_path import ensure_data_file


class AppointmentMainWindowEx(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.file_path = ensure_data_file("datasets/bookings.json")

        self.current_row = None
        self.new_status = None
        self.current_booking_id = None

        self.setupBackButtonStyle()
        self.setupSignal()
        self.loadTable()

    def setupBackButtonStyle(self):
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
            text-align: left;
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

    def setupSignal(self):
        self.pushButtonAdd.clicked.connect(self.openAddWindow)
        self.pushButtonClearFilters.clicked.connect(self.clearFilters)

        self.pushButtonConfirmed.clicked.connect(self.filterConfirmed)
        self.pushButtonPending.clicked.connect(self.filterPending)

        self.search_box.textChanged.connect(self.searchBooking)
        self.dateEdit.dateChanged.connect(self.filterByDate)

        self.pushButtonConfirm.clicked.connect(self.selectConfirmed)
        self.pushButtonCancel.clicked.connect(self.selectCancel)

        self.pushButtonEdit.clicked.connect(self.editBooking)
        self.tableWidgetBooking.cellClicked.connect(self.showDetail)
        self.pushButtonBack.clicked.connect(self.goBack)

    def read_bookings_data(self):
        if not os.path.exists(self.file_path):
            return {"bookings": []}

        try:
            with open(self.file_path, encoding="utf8") as f:
                data = json.load(f)
        except Exception:
            return {"bookings": []}

        if isinstance(data, list):
            return {"bookings": data}

        if "bookings" not in data or not isinstance(data["bookings"], list):
            data["bookings"] = []

        return data

    def write_bookings_data(self, data):
        with open(self.file_path, "w", encoding="utf8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def loadTable(self):
        data = self.read_bookings_data()
        bookings = data.get("bookings", [])
        bookings.sort(key=lambda x: x.get("created_at", ""), reverse=True)

        today = datetime.now().strftime("%Y-%m-%d")

        self.tableWidgetBooking.setRowCount(len(bookings))

        for row, b in enumerate(bookings):
            self.tableWidgetBooking.setItem(row, 0, QTableWidgetItem(str(b.get("booking_id", ""))))
            self.tableWidgetBooking.setItem(row, 1, QTableWidgetItem(str(b.get("name", ""))))
            self.tableWidgetBooking.setItem(row, 2, QTableWidgetItem(str(b.get("phone", ""))))
            self.tableWidgetBooking.setItem(row, 3, QTableWidgetItem(str(b.get("date", ""))))
            self.tableWidgetBooking.setItem(row, 4, QTableWidgetItem(str(b.get("time", ""))))
            self.tableWidgetBooking.setItem(row, 5, QTableWidgetItem(str(b.get("package", ""))))
            self.tableWidgetBooking.setItem(row, 6, QTableWidgetItem(str(b.get("concept", ""))))
            self.tableWidgetBooking.setItem(row, 7, QTableWidgetItem(str(b.get("location", ""))))

            status = b.get("status", "Pending")
            status_item = QTableWidgetItem(status)

            if status == "Confirmed":
                status_item.setBackground(QColor(200, 255, 200))
            elif status == "Pending":
                status_item.setBackground(QColor(255, 230, 200))
            elif status == "Cancelled":
                status_item.setBackground(QColor(255, 200, 200))

            self.tableWidgetBooking.setItem(row, 8, status_item)
            self.tableWidgetBooking.setItem(row, 9, QTableWidgetItem(str(b.get("created_at", ""))))

            if b.get("date") == today:
                for col in range(10):
                    item = self.tableWidgetBooking.item(row, col)
                    if item:
                        item.setBackground(QColor(220, 240, 255))

        self.tableWidgetBooking.setSelectionBehavior(
            self.tableWidgetBooking.SelectionBehavior.SelectRows
        )

    def showDetail(self, row, column):
        item = self.tableWidgetBooking.item(row, 0)
        if not item:
            return

        booking_id = item.text()
        data = self.read_bookings_data()
        bookings = data.get("bookings", [])

        booking = None
        for b in bookings:
            if b.get("booking_id") == booking_id:
                booking = b
                break

        if not booking:
            return

        self.current_booking_id = booking_id
        self.new_status = None

        self.lineEditName.setText(str(booking.get("name", "")))
        self.lineEditEmail.setText(str(booking.get("email", "")))
        self.lineEditPhone.setText(str(booking.get("phone", "")))

        self.lineEditDate.setText(str(booking.get("date", "")))
        self.lineEditTime.setText(str(booking.get("time", "")))
        self.lineEditLocation.setText(str(booking.get("location", "")))

        self.lineEditPackage.setText(str(booking.get("package", "")))
        self.lineEditConcept.setText(str(booking.get("concept", "")))
        self.lineEditPromo.setText(str(booking.get("promo", "")))
        self.lineEditNote.setText(str(booking.get("notes", "")))

        status = booking.get("status", "Pending")

        self.radioButtonConfirmed.setChecked(status == "Confirmed")
        self.radioButtonCancel.setChecked(status == "Cancelled")
        self.radioButtonPending.setChecked(status not in ["Confirmed", "Cancelled"])

    def selectConfirmed(self):
        if not self.current_booking_id:
            QMessageBox.warning(self, "Warning", "Please select a booking.")
            return

        self.new_status = "Confirmed"
        self.radioButtonConfirmed.setChecked(True)

    def selectCancel(self):
        if not self.current_booking_id:
            QMessageBox.warning(self, "Warning", "Please select a booking.")
            return

        reply = QMessageBox.question(
            self,
            "Confirm Cancel",
            "Are you sure you want to cancel this booking?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.new_status = "Cancelled"
            self.radioButtonCancel.setChecked(True)

    def editBooking(self):
        if not self.current_booking_id:
            QMessageBox.warning(self, "Warning", "Please select a booking.")
            return

        data = self.read_bookings_data()

        for booking in data["bookings"]:
            if booking.get("booking_id") == self.current_booking_id:
                booking["name"] = self.lineEditName.text().strip()
                booking["email"] = self.lineEditEmail.text().strip()
                booking["phone"] = self.lineEditPhone.text().strip()

                booking["date"] = self.lineEditDate.text().strip()
                booking["time"] = self.lineEditTime.text().strip()
                booking["location"] = self.lineEditLocation.text().strip()

                booking["package"] = self.lineEditPackage.text().strip()
                booking["concept"] = self.lineEditConcept.text().strip()
                booking["promo"] = self.lineEditPromo.text().strip()
                booking["notes"] = self.lineEditNote.text().strip()

                if self.new_status:
                    booking["status"] = self.new_status
                break

        self.write_bookings_data(data)

        QMessageBox.information(self, "Success", "Booking updated successfully.")
        self.loadTable()

    def searchBooking(self):
        keyword = self.search_box.text().lower().strip()

        for row in range(self.tableWidgetBooking.rowCount()):
            match_found = False

            for col in range(self.tableWidgetBooking.columnCount()):
                item = self.tableWidgetBooking.item(row, col)
                if item and keyword in item.text().lower():
                    match_found = True
                    break

            self.tableWidgetBooking.setRowHidden(row, not match_found)

    def filterConfirmed(self):
        for row in range(self.tableWidgetBooking.rowCount()):
            item = self.tableWidgetBooking.item(row, 8)
            if item:
                self.tableWidgetBooking.setRowHidden(row, item.text() != "Confirmed")

    def filterPending(self):
        for row in range(self.tableWidgetBooking.rowCount()):
            item = self.tableWidgetBooking.item(row, 8)
            if item:
                self.tableWidgetBooking.setRowHidden(row, item.text() != "Pending")

    def filterByDate(self):
        selected_date = self.dateEdit.date().toString("yyyy-MM-dd")

        for row in range(self.tableWidgetBooking.rowCount()):
            item = self.tableWidgetBooking.item(row, 3)
            if item:
                self.tableWidgetBooking.setRowHidden(row, item.text() != selected_date)

    def clearFilters(self):
        self.search_box.clear()

        for row in range(self.tableWidgetBooking.rowCount()):
            self.tableWidgetBooking.setRowHidden(row, False)

    def openAddWindow(self):
        from Lumora_Studio_Booking_System.admin_ui.add_appoint.ui.AddAppointmentMainWindowEx import AddAppointmentMainWindowEx

        self.addWindow = AddAppointmentMainWindowEx(self)
        self.addWindow.show()

    def goBack(self):
        from Lumora_Studio_Booking_System.admin_ui.home_admin.ui.AdminHomeMainWindowEx import AdminHomeMainWindowEx

        self.homeWindow = AdminHomeMainWindowEx()
        self.homeWindow.show()
        self.close()