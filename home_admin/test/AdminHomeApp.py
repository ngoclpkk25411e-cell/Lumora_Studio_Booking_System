import sys
from PyQt6.QtWidgets import QApplication

from Lumora_Studio_Booking_System.admin_ui.home_admin.ui.AdminHomeMainWindowEx import AdminHomeMainWindowEx


app = QApplication(sys.argv)

gui = AdminHomeMainWindowEx()
gui.show()

sys.exit(app.exec())