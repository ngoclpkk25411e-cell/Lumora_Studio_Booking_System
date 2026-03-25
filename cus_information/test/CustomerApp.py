import sys
from PyQt6.QtWidgets import QApplication

from Lumora_Studio_Booking_System.admin_ui.cus_information.ui.CustomerMainWindowEx import CustomerMainWindowEx

app = QApplication(sys.argv)

window = CustomerMainWindowEx()
window.show()

sys.exit(app.exec())