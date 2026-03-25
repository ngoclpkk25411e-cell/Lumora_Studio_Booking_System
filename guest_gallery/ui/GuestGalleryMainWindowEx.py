import os
import sys

from PyQt6.QtCore import QPropertyAnimation, Qt
from PyQt6.QtGui import QPixmap, QCursor
from PyQt6.QtWidgets import QMainWindow

from .GuestGalleryMainWindow import Ui_MainWindow


def resource_path(relative_path: str) -> str:
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)

    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
    return os.path.join(base_path, relative_path)


class GuestGalleryMainWindowEx(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.setupBackButtonStyle()
        self.setupImages()
        self.setupConceptClicks()
        self.setupHoverEffect()

        self.pushButtonBack.clicked.connect(self.goHome)
        self.pushButtonBack.pressed.connect(self.animateBack)

    def setupBackButtonStyle(self):
        self.pushButtonBack.setText("Back")
        self.pushButtonBack.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            color: black;
            border: none;
            font-size: 16px;
            padding: 6px 14px;
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

    def find_first_image(self, folder_relative_path: str):
        folder_path = resource_path(folder_relative_path)
        if not os.path.isdir(folder_path):
            print(f"[Missing folder] {folder_path}")
            return None

        exts = (".png", ".jpg", ".jpeg", ".webp", ".bmp")
        files = sorted(
            f for f in os.listdir(folder_path)
            if f.lower().endswith(exts)
        )

        if not files:
            print(f"[No image found] {folder_path}")
            return None

        return os.path.join(folder_path, files[0])

    def set_label_image(self, label, image_path, keep_ratio=True):
        if label is None or not image_path or not os.path.exists(image_path):
            return

        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            print(f"[Cannot load image] {image_path}")
            return

        w = max(label.width(), 100)
        h = max(label.height(), 100)

        if keep_ratio:
            pixmap = pixmap.scaled(
                w, h,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
        else:
            pixmap = pixmap.scaled(
                w, h,
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setScaledContents(True)

    def setupImages(self):
        profile_img = self.find_first_image("guest_ui/guest_gallery/images/Profile")
        prewedding_img = self.find_first_image("guest_ui/guest_gallery/images/PreWedding")
        portrait_img = self.find_first_image("guest_ui/guest_gallery/images/Portrait")
        generation_img = self.find_first_image("guest_ui/guest_gallery/images/Generation")
        birthday_img = self.find_first_image("guest_ui/guest_gallery/images/Birthday")

        logo_path = resource_path("guest_ui/guest_gallery/images/logo.png")

        self.set_label_image(getattr(self, "labelProfile", None), profile_img)
        self.set_label_image(getattr(self, "labelPreWedding", None), prewedding_img)
        self.set_label_image(getattr(self, "labelPortrait", None), portrait_img)
        self.set_label_image(getattr(self, "labelGeneration", None), generation_img)
        self.set_label_image(getattr(self, "labelBirthday", None), birthday_img)

        for name in ["labelLogo", "label_logo", "label_Logo", "label"]:
            lb = getattr(self, name, None)
            if lb and os.path.exists(logo_path):
                self.set_label_image(lb, logo_path, keep_ratio=True)
                break

    def bind_click(self, label, handler):
        if label is None:
            return
        label.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        label.mousePressEvent = handler

    def setupConceptClicks(self):
        self.bind_click(getattr(self, "labelProfile", None), self.openProfileGallery)
        self.bind_click(getattr(self, "labelPreWedding", None), self.openPreWeddingGallery)
        self.bind_click(getattr(self, "labelPortrait", None), self.openPortraitGallery)
        self.bind_click(getattr(self, "labelGeneration", None), self.openGenerationGallery)
        self.bind_click(getattr(self, "labelBirthday", None), self.openBirthdayGallery)

    def setupHoverEffect(self):
        labels = [
            getattr(self, "labelProfile", None),
            getattr(self, "labelPreWedding", None),
            getattr(self, "labelPortrait", None),
            getattr(self, "labelGeneration", None),
            getattr(self, "labelBirthday", None)
        ]

        for label in labels:
            if label is None:
                continue
            label.original_geometry = label.geometry()
            label.enterEvent = lambda e, l=label: self.zoomIn(l)
            label.leaveEvent = lambda e, l=label: self.zoomOut(l)

    def zoomIn(self, label):
        self.anim = QPropertyAnimation(label, b"geometry")
        rect = label.geometry()
        self.anim.setDuration(150)
        self.anim.setStartValue(rect)
        self.anim.setEndValue(rect.adjusted(-5, -5, 5, 5))
        self.anim.start()

        label.setStyleSheet("""
        border: 2px solid #C9A27C;
        border-radius: 10px;
        """)

    def zoomOut(self, label):
        self.anim = QPropertyAnimation(label, b"geometry")
        self.anim.setDuration(150)
        self.anim.setStartValue(label.geometry())
        self.anim.setEndValue(label.original_geometry)
        self.anim.start()
        label.setStyleSheet("")

    def animateBack(self):
        self.anim = QPropertyAnimation(self.pushButtonBack, b"geometry")
        rect = self.pushButtonBack.geometry()
        self.anim.setDuration(120)
        self.anim.setStartValue(rect)
        self.anim.setEndValue(rect.adjusted(2, 2, -2, -2))
        self.anim.start()

    def openProfileGallery(self, event):
        from Lumora_Studio_Booking_System.guest_ui.guest_gallery.ui.Concept_ProfileEx import ConceptProfileWindow
        self.gallery = ConceptProfileWindow()
        self.gallery.show()
        self.close()

    def openPreWeddingGallery(self, event):
        from Lumora_Studio_Booking_System.guest_ui.guest_gallery.ui.Concept_PreWeddingEx import ConceptPreWeddingWindow
        self.gallery = ConceptPreWeddingWindow()
        self.gallery.show()
        self.close()

    def openPortraitGallery(self, event):
        from Lumora_Studio_Booking_System.guest_ui.guest_gallery.ui.Concept_PortraitEx import ConceptPortraitWindow
        self.gallery = ConceptPortraitWindow()
        self.gallery.show()
        self.close()

    def openGenerationGallery(self, event):
        from Lumora_Studio_Booking_System.guest_ui.guest_gallery.ui.Concept_GenerationEx import ConceptGenerationWindow
        self.gallery = ConceptGenerationWindow()
        self.gallery.show()
        self.close()

    def openBirthdayGallery(self, event):
        from Lumora_Studio_Booking_System.guest_ui.guest_gallery.ui.Concept_BirthdayEx import ConceptBirthdayWindow
        self.gallery = ConceptBirthdayWindow()
        self.gallery.show()
        self.close()

    def goHome(self):
        from Lumora_Studio_Booking_System.guest_ui.home.ui.HomeMainWindowEx import HomeMainWindowEx
        self.home = HomeMainWindowEx()
        self.home.show()
        self.close()