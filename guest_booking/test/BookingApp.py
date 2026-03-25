import sys
from PyQt6.QtWidgets import QApplication
from guest_ui.guest_booking.ui.BookingMainWindowEx import BookingMainWindowEx

app = QApplication(sys.argv)
window = BookingMainWindowEx()
window.show()
app.exec()