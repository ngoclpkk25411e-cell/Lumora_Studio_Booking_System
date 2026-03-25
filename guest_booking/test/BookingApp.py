import sys
from PyQt6.QtWidgets import QApplication

from Lumora_Studio_Booking_System.guest_ui.guest_booking.ui.BookingMainWindowEx import BookingMainWindowEx

app = QApplication(sys.argv)
window = BookingMainWindowEx()
window.show()
app.exec()