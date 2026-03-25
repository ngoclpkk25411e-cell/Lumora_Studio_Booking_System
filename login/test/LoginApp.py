import sys
from PyQt6.QtWidgets import QApplication

from Lumora_Studio_Booking_System.admin_ui.login.ui.LoginMainWindowEx import LoginMainWindowEx

app = QApplication(sys.argv)
window = LoginMainWindowEx()
window.show()
sys.exit(app.exec())