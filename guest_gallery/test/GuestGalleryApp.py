import sys
from PyQt6.QtWidgets import QApplication
from Lumora_Studio_Booking_System.guest_ui.guest_gallery.ui.GuestGalleryMainWindowEx import GuestGalleryMainWindowEx

app = QApplication(sys.argv)
gui = GuestGalleryMainWindowEx()
gui.show()
sys.exit(app.exec())