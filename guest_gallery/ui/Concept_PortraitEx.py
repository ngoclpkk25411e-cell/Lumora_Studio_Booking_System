import sys
import os

from PyQt6.QtCore import QPropertyAnimation
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QPixmap, QIcon

from .Concept_Portrait import Ui_MainWindow


def resource_path(relative_path: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)

    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
    return os.path.join(base_path, relative_path)


class ConceptPortraitWindow(QMainWindow, Ui_MainWindow):
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
        image_dir = resource_path("guest_ui/guest_gallery/images/Portrait")

        images = [
            "625020464_17986243661930408_4203013993903022732_n.jpg",
            "487414056_635042436183746_6697205309929125131_n.jpg",
            "638313366_17989136837930408_7086427777565813361_n.jpg",
            "630024908_17987933759930408_7914660855801865906_n.jpg",
            "613705475_17984731358930408_5059974921820876885_n.jpg",
            "641534800_17988921755930408_7753007074676520363_n.jpg"
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
    window = ConceptPortraitWindow()
    window.show()
    sys.exit(app.exec())