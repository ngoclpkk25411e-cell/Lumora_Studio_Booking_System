import sys
from PyQt6.QtWidgets import QApplication

from Lumora_Studio_Booking_System.admin_ui.managing_booking.ui.AppointmentMainWindowEx import AppointmentMainWindowEx

app = QApplication(sys.argv)

window = AppointmentMainWindowEx()
window.show()

sys.exit(app.exec())