import sys
from PyQt6.QtWidgets import QApplication

from Lumora_Studio_Booking_System.guest_ui.after_booking.ui.AfterBookingMainWindowEx import AfterBookingMainWindowEx

app = QApplication(sys.argv)

# để None vì sẽ truyền từ Booking khi chạy thật
window = AfterBookingMainWindowEx({})

window.show()

sys.exit(app.exec())