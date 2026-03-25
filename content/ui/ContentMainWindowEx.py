import os
import json

from PyQt6.QtWidgets import (
    QMainWindow,
    QLabel,
    QFileDialog,
    QMessageBox,
    QFrame,
    QVBoxLayout
)

from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize

from admin_ui.content.ui.ContentMainWindow import Ui_MainWindow


class ContentMainWindowEx(QMainWindow, Ui_MainWindow):

    def __init__(self):

        super().__init__()

        self.setupUi(self)

        # ===== PROJECT ROOT =====
        self.base_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(__file__)
                )
            )
        )

        # ⭐ FIX ICON PATH (QUAN TRỌNG)
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.icon_folder = os.path.join(BASE_DIR, "..", "images")

        # ===== DATA PATH =====
        self.gallery_folder = os.path.join(
            self.base_dir,
            "guest_ui",
            "guest_gallery",
            "images"
        )

        self.gallery_json = os.path.join(
            self.base_dir,
            "datasets",
            "gallery.json"
        )

        self.review_path = os.path.join(
            self.base_dir,
            "datasets",
            "reviews.json"
        )

        self.selected_photo = None
        self.selected_review = None

        # ===== SET ICONS =====
        self.setupIcons()

        self.setupAlbums()
        self.setupSignals()

        self.loadGallery()
        self.loadReviews()
        self.setupRatingComboBox()

    # =========================
    # ICONS (FIX FULL)
    # =========================
    def setupIcons(self):

        add_icon = os.path.join(self.icon_folder, "add.png")
        delete_icon = os.path.join(self.icon_folder, "bin.png")

        # ADD ICON
        if os.path.exists(add_icon):
            self.label_add_photo.setPixmap(
                QPixmap(add_icon).scaled(
                    40, 40,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )
        else:
            print("❌ Missing:", add_icon)

        # DELETE ICON
        if os.path.exists(delete_icon):

            icon = QIcon(delete_icon)

            self.pushButtonDeletePhoto.setIcon(icon)
            self.pushButtonDeletePhoto.setIconSize(QSize(28, 28))

            self.pushButtonDeleteReview.setIcon(icon)
            self.pushButtonDeleteReview.setIconSize(QSize(28, 28))

        else:
            print("❌ Missing:", delete_icon)

    # =========================
    # RATING COMBOBOX
    # =========================
    def setupRatingComboBox(self):

        self.comboBoxRating.clear()

        self.comboBoxRating.addItems([
            "View All",
            "5 Stars",
            "4 Stars",
            "3 Stars",
            "2 Stars",
            "1 Star"
        ])

    # =========================
    # SIGNAL
    # =========================
    def setupSignals(self):

        self.comboBoxAlb.currentIndexChanged.connect(self.loadGallery)

        self.pushButtonSavePhoto.clicked.connect(self.addPhoto)

        self.pushButtonDeletePhoto.clicked.connect(self.deletePhoto)

        self.pushButtonDeleteReview.clicked.connect(self.deleteReview)

        self.comboBoxRating.currentIndexChanged.connect(self.filterReviews)

        self.pushButtonBack.clicked.connect(self.goBack)

        self.label_add_photo.mousePressEvent = self.addPhoto

    # =========================
    # LOAD ALBUMS
    # =========================
    def setupAlbums(self):

        self.comboBoxAlb.clear()

        if not os.path.exists(self.gallery_folder):
            return

        for folder in os.listdir(self.gallery_folder):

            path = os.path.join(self.gallery_folder, folder)

            if os.path.isdir(path):
                self.comboBoxAlb.addItem(folder)

    # =========================
    # LOAD GALLERY
    # =========================
    def loadGallery(self):

        album = self.comboBoxAlb.currentText()

        album_path = os.path.join(self.gallery_folder, album)

        labels = [
            self.label_photo1,
            self.label_photo2,
            self.label_photo3,
            self.label_photo4,
            self.label_photo5,
            self.label_photo6
        ]

        for label in labels:
            label.clear()

        if not os.path.exists(album_path):
            return

        images = [
            f for f in os.listdir(album_path)
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
        ]

        for label, img in zip(labels, images):

            path = os.path.join(album_path, img)

            pix = QPixmap(path)

            pix = pix.scaled(
                180,
                180,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )

            label.setPixmap(pix)
            label.setFixedSize(180, 180)
            label.setScaledContents(True)

            label.mousePressEvent = lambda e, p=path: self.selectPhoto(p)

    # =========================
    # SELECT PHOTO
    # =========================
    def selectPhoto(self, path):

        self.selected_photo = path

    # =========================
    # ADD PHOTO
    # =========================
    def addPhoto(self, event=None):

        album = self.comboBoxAlb.currentText()

        album_path = os.path.join(self.gallery_folder, album)

        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Images (*.jpg *.jpeg *.png *.webp)"
        )

        if not file:
            return

        name = os.path.basename(file)

        new_path = os.path.join(album_path, name)

        with open(file, "rb") as src:
            with open(new_path, "wb") as dst:
                dst.write(src.read())

        self.updateGalleryJson(album, name)

        self.loadGallery()

    # =========================
    # DELETE PHOTO
    # =========================
    def deletePhoto(self):

        if not self.selected_photo:

            QMessageBox.warning(
                self,
                "Warning",
                "Please select photo first"
            )
            return

        os.remove(self.selected_photo)

        self.selected_photo = None

        self.loadGallery()

    # =========================
    # UPDATE JSON
    # =========================
    def updateGalleryJson(self, album, image):

        if not os.path.exists(self.gallery_json):
            return

        with open(self.gallery_json, encoding="utf8") as f:
            data = json.load(f)

        for alb in data["albums"]:

            if alb["name"].lower() == album.lower():

                alb["images"].append(f"{album}/{image}")

        with open(self.gallery_json, "w", encoding="utf8") as f:
            json.dump(data, f, indent=4)

    # =========================
    # LOAD REVIEWS
    # =========================
    def loadReviews(self):

        if not os.path.exists(self.review_path):
            self.reviews = []
            return

        with open(self.review_path, encoding="utf8") as f:

            data = json.load(f)

        self.reviews = data.get("reviews", [])

        self.displayReviews(self.reviews)

    # =========================
    # DISPLAY REVIEWS
    # =========================
    def displayReviews(self, reviews):

        layout = self.verticalLayout_5

        for i in reversed(range(layout.count())):

            widget = layout.itemAt(i).widget()

            if widget:
                widget.deleteLater()

        for review in reviews:

            frame = QFrame()

            frame.setStyleSheet("""
            QFrame{
                border:2px solid #C9A27C;
                background:#FFF8F0;
                padding:15px;
            }
            """)

            stars = "⭐" * review.get("rating", 0)

            text = f"""
Name: {review['name']}
Email: {review['email']}
Rating: {stars}

Review:
{review['review']}
"""

            label = QLabel(text)

            label.setWordWrap(True)

            layout_card = QVBoxLayout(frame)

            layout_card.addWidget(label)

            frame.mousePressEvent = lambda e, r=review: self.selectReview(r)

            layout.addWidget(frame)

    # =========================
    # SELECT REVIEW
    # =========================
    def selectReview(self, review):

        self.selected_review = review

    # =========================
    # FILTER REVIEWS
    # =========================
    def filterReviews(self):

        text = self.comboBoxRating.currentText()

        if text == "View All":
            filtered = self.reviews
        else:

            stars = int(text[0])

            filtered = [
                r for r in self.reviews
                if r["rating"] == stars
            ]

        self.displayReviews(filtered)

    # =========================
    # DELETE REVIEW
    # =========================
    def deleteReview(self):

        if not self.selected_review:

            QMessageBox.warning(
                self,
                "Warning",
                "Select review first"
            )
            return

        with open(self.review_path, encoding="utf8") as f:

            data = json.load(f)

        reviews = data.get("reviews", [])

        reviews = [
            r for r in reviews
            if r != self.selected_review
        ]

        data["reviews"] = reviews

        with open(self.review_path, "w", encoding="utf8") as f:

            json.dump(data, f, indent=4)

        self.loadReviews()

    # =========================
    # BACK
    # =========================
    def goBack(self):

        from admin_ui.home_admin.ui.AdminHomeMainWindowEx import AdminHomeMainWindowEx

        self.home = AdminHomeMainWindowEx()

        self.home.show()

        self.close()