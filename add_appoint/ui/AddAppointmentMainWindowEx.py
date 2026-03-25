import json
import os
from datetime import datetime

from PyQt6.QtWidgets import QMainWindow, QMessageBox

from Lumora_Studio_Booking_System.admin_ui.add_appoint.ui.AddAppointmentMainWindow import Ui_MainWindow
from Lumora_Studio_Booking_System.utils_path import ensure_data_file


class AddAppointmentMainWindowEx(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__()

        self.setupUi(self)
        self.setupCombobox()

        self.parent = parent
        self.file_path = ensure_data_file("datasets/bookings.json")

        self.pushButtonAdd.clicked.connect(self.saveBooking)

    def setupCombobox(self):
        self.comboBoxPackage.clear()
        self.comboBoxPackage.addItems([
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
            "Outdoor / Nature"
        ])

        self.comboBoxQuantity.clear()
        self.comboBoxQuantity.addItems([
            "1", "2", "3", "4", "5", "6", "7",
            "More (please specify in notes)"
        ])

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

    def generate_next_booking_id(self, bookings):
        max_num = 0

        for booking in bookings:
            booking_id = str(booking.get("booking_id", ""))
            if booking_id.startswith("B"):
                try:
                    num = int(booking_id[1:])
                    if num > max_num:
                        max_num = num
                except Exception:
                    pass

        return f"B{max_num + 1:03d}"

    def saveBooking(self):
        name = self.lineEditName_2.text().strip()
        email = self.lineEditEmail_2.text().strip()
        phone = self.lineEditPhone_2.text().strip()

        date = self.dateEdit.date().toString("yyyy-MM-dd")
        time = self.timeEdit.time().toString("HH:mm")

        concept = self.comboBoxConcept.currentText()
        package_name = self.comboBoxPackage.currentText()
        location = self.comboBoxLocation.currentText()
        quantity = self.comboBoxQuantity.currentText()

        promo = self.lineEditPromo.text().strip()
        notes = self.lineEditNotes.text().strip()

        if name == "" or phone == "":
            QMessageBox.warning(self, "Warning", "Please fill required fields")
            return

        text = f"""
Confirm adding appointment?

Name: {name}
Phone: {phone}
Date: {date}
Time: {time}
Concept: {concept}
Package: {package_name}
Location: {location}
Quantity: {quantity}
"""

        reply = QMessageBox.question(
            self,
            "Confirm Adding",
            text,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.No:
            return

        data = self.read_bookings_data()
        bookings = data.get("bookings", [])

        new_id = self.generate_next_booking_id(bookings)
        created_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        new_booking = {
            "booking_id": new_id,
            "name": name,
            "email": email,
            "phone": phone,
            "date": date,
            "time": time,
            "concept": concept,
            "location": location,
            "number_people": quantity,
            "package": package_name,
            "notes": notes,
            "promo": promo,
            "status": "Confirmed",
            "created_at": created_time
        }

        bookings.append(new_booking)
        data["bookings"] = bookings

        self.write_bookings_data(data)

        QMessageBox.information(self, "Success", "Appointment Added")

        if self.parent is not None:
            try:
                self.parent.loadTable()
            except Exception:
                pass

        self.close()