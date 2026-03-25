import sys
import os

from PyQt6.QtCore import QPropertyAnimation, Qt
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPixmap, QIcon

from .Concept_Birthday import Ui_MainWindow


def resource_path(relative_path: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)

    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
    return os.path.join(base_path, relative_path)


class ConceptBirthdayWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setupBackButtonStyle()
        self.show_images()

        self.pushButtonBack.clicked.connect(self.goBackGallery)
        self.pushButtonBack.pressed.connect(self.animateBack)

    def setupBackButtonStyle(self):
        self.pushButtonBack.setText("Back")
        self.pushButtonBack.setIcon(QIcon())
        self.pushButtonBack.setMinimumSize(90, 34)
        self.pushButtonBack.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            color: black;
            border: none;
            border-radius: 0px;
            font-size: 15px;
            padding: 6px 18px;
            text-align: center;
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

    def animateBack(self):
        self.anim = QPropertyAnimation(self.pushButtonBack, b"geometry")
        rect = self.pushButtonBack.geometry()

        self.anim.setDuration(120)
        self.anim.setStartValue(rect)
        self.anim.setEndValue(rect.adjusted(2, 2, -2, -2))
        self.anim.start()

    def set_image_to_label(self, label, img_path):
        if not os.path.exists(img_path):
            print("Image not found:", img_path)
            return

        pixmap = QPixmap(img_path)
        if pixmap.isNull():
            print("Cannot load image:", img_path)
            return

        label.setPixmap(pixmap)
        label.setScaledContents(True)

    def show_images(self):
        image_dir = resource_path("guest_ui/guest_gallery/images/Birthday")

        images = [
            "642709375_17990564156930408_7673910412112228190_n.jpg",
            "480903552_1168905471689068_2882378151523049373_n.jpg",
            "649215306_17990564165930408_164478230355821732_n.jpg",
            "649537342_17990564141930408_3741802768060329672_n.jpg",
            "487140309_635042446183745_951480232530720696_n.jpg",
            "649599929_17990564123930408_8733319181847484524_n.jpg"
        ]

        labels = [
            self.label,
            self.label_2,
            self.label_3,
            self.label_4,
            self.label_5,
            self.label_6
        ]

        for label, img in zip(labels, images):
            img_path = os.path.join(image_dir, img)
            self.set_image_to_label(label, img_path)

    def goBackGallery(self):
        from Lumora_Studio_Booking_System.guest_ui.guest_gallery.ui.GuestGalleryMainWindowEx import GuestGalleryMainWindowEx

        self.gallery = GuestGalleryMainWindowEx()
        self.gallery.show()
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConceptBirthdayWindow()
    window.show()
    sys.exit(app.exec())