import os
import json
import shutil

from PyQt6.QtWidgets import (
    QMainWindow,
    QLabel,
    QFileDialog,
    QMessageBox,
    QFrame,
    QVBoxLayout
)
from PyQt6.QtGui import QPixmap, QIcon, QFont
from PyQt6.QtCore import Qt, QSize

from Lumora_Studio_Booking_System.admin_ui.content.ui.ContentMainWindow import Ui_MainWindow
from Lumora_Studio_Booking_System.admin_ui.home_admin.ui.AdminHomeMainWindowEx import AdminHomeMainWindowEx
from Lumora_Studio_Booking_System.utils_path import (
    resource_path,
    writable_data_path,
    ensure_data_file,
)


class ContentMainWindowEx(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # chỉ đọc icon từ bundle
        self.icon_folder = resource_path("admin_ui/home_admin/images")

        # ghi thật vào thư mục cạnh exe / project
        self.gallery_folder = writable_data_path("guest_ui/guest_gallery/images")
        self.gallery_json = ensure_data_file("datasets/gallery.json")
        self.review_path = ensure_data_file("datasets/reviews.json")

        self.selected_photo = None
        self.selected_review = None
        self.reviews = []

        self.ensure_gallery_folders()

        self.applyModernStyle()
        self.setupIcons()
        self.setupAlbums()
        self.setupSignals()

        self.loadGallery()
        self.loadReviews()
        self.setupRatingComboBox()

    def ensure_gallery_folders(self):
        os.makedirs(self.gallery_folder, exist_ok=True)

        default_albums = ["Birthday", "Generation", "Portrait", "PreWedding", "Profile"]
        for album in default_albums:
            os.makedirs(os.path.join(self.gallery_folder, album), exist_ok=True)

        # nếu thư mục ảnh ngoài chưa có dữ liệu thì copy từ bundle ra
        bundled_gallery = resource_path("guest_ui/guest_gallery/images")
        if os.path.exists(bundled_gallery):
            for album in os.listdir(bundled_gallery):
                src_album = os.path.join(bundled_gallery, album)
                dst_album = os.path.join(self.gallery_folder, album)

                if os.path.isdir(src_album):
                    os.makedirs(dst_album, exist_ok=True)

                    src_images = [
                        f for f in os.listdir(src_album)
                        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
                    ]
                    dst_images = [
                        f for f in os.listdir(dst_album)
                        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
                    ]

                    if not dst_images:
                        for img in src_images:
                            src_img = os.path.join(src_album, img)
                            dst_img = os.path.join(dst_album, img)
                            if not os.path.exists(dst_img):
                                shutil.copy2(src_img, dst_img)

    def applyModernStyle(self):
        self.setStyleSheet("""
        QMainWindow, QWidget {
            background-color: #F7F1EA;
            color: #6B3F1D;
            font-family: "Times New Roman";
            font-size: 14px;
        }

        QLabel {
            color: #6B3F1D;
            font-size: 14px;
            background: transparent;
        }

        QPushButton {
            background-color: #F3E7D8;
            color: #7A4A22;
            border: 1.5px solid #A97B50;
            border-radius: 18px;
            padding: 8px 14px;
            font-size: 15px;
            font-weight: 600;
            min-height: 18px;
        }

        QPushButton:hover {
            background-color: #EAD9C5;
        }

        QPushButton:pressed {
            background-color: #DFC9B1;
        }

        QComboBox {
            background-color: #FFF9F3;
            color: #6B3F1D;
            border: 1.5px solid #A97B50;
            border-radius: 14px;
            padding: 8px 12px;
            font-size: 15px;
            font-weight: 600;
        }

        QComboBox QAbstractItemView {
            background-color: #FFF9F3;
            color: #6B3F1D;
            border: 1px solid #A97B50;
            selection-background-color: #EAD9C5;
            selection-color: #6B3F1D;
            outline: 0;
        }

        QScrollArea {
            background: transparent;
            border: none;
        }

        QFrame {
            background-color: #FFF9F3;
            border: 2px solid #B78B60;
            border-radius: 22px;
        }
        """)

        for widget in [
            getattr(self, "comboBoxAlb", None),
            getattr(self, "comboBoxRating", None),
            getattr(self, "pushButtonDeletePhoto", None),
            getattr(self, "pushButtonSavePhoto", None),
            getattr(self, "pushButtonDeleteReview", None),
            getattr(self, "pushButtonBack", None),
        ]:
            if widget is not None:
                font = QFont("Times New Roman", 15)
                font.setBold(True)
                widget.setFont(font)

        self.pushButtonBack.setStyleSheet("""
        QPushButton {
            background: transparent;
            color: black;
            border: none;
            font-family: "Times New Roman";
            font-size: 15px;
            font-weight: 700;
            padding: 6px 18px;
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

        self.label.setStyleSheet("""
        QLabel {
            background: transparent;
            color: #6B3F1D;
            border: none;
            font-family: "Times New Roman";
            font-size: 30px;
            font-weight: 700;
            padding: 0px;
            margin: 0px;
        }
        """)

    def setupIcons(self):
        add_icon = os.path.join(self.icon_folder, "add.png")
        delete_icon = os.path.join(self.icon_folder, "bin.png")

        if os.path.exists(add_icon):
            self.label_add_photo.setPixmap(
                QPixmap(add_icon).scaled(
                    36, 36,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
            )

        if os.path.exists(delete_icon):
            self.pushButtonDeletePhoto.setIcon(QIcon(delete_icon))
            self.pushButtonDeletePhoto.setIconSize(QSize(20, 20))

            self.pushButtonDeleteReview.setIcon(QIcon(delete_icon))
            self.pushButtonDeleteReview.setIconSize(QSize(20, 20))

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

    def setupSignals(self):
        self.comboBoxAlb.currentIndexChanged.connect(self.loadGallery)
        self.pushButtonSavePhoto.clicked.connect(self.addPhoto)
        self.pushButtonDeletePhoto.clicked.connect(self.deletePhoto)
        self.pushButtonDeleteReview.clicked.connect(self.deleteReview)
        self.comboBoxRating.currentIndexChanged.connect(self.filterReviews)
        self.pushButtonBack.clicked.connect(self.goBack)
        self.label_add_photo.mousePressEvent = self.addPhoto

    def setupAlbums(self):
        self.comboBoxAlb.clear()

        if not os.path.exists(self.gallery_folder):
            return

        for folder in sorted(os.listdir(self.gallery_folder)):
            path = os.path.join(self.gallery_folder, folder)
            if os.path.isdir(path):
                self.comboBoxAlb.addItem(folder)

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
            label.setStyleSheet("""
                QLabel {
                    border: 2px solid #C69C72;
                    background-color: #FFF9F3;
                    border-radius: 10px;
                }
            """)
            label.setFixedSize(180, 180)

        if not os.path.exists(album_path):
            return

        images = sorted([
            f for f in os.listdir(album_path)
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
        ])

        for label, img in zip(labels, images):
            path = os.path.join(album_path, img)
            pix = QPixmap(path).scaled(
                180,
                180,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )

            label.setPixmap(pix)
            label.setScaledContents(True)
            label.mousePressEvent = lambda e, p=path, lb=label: self.selectPhoto(p, lb)

    def selectPhoto(self, path, selected_label=None):
        self.selected_photo = path

        labels = [
            self.label_photo1,
            self.label_photo2,
            self.label_photo3,
            self.label_photo4,
            self.label_photo5,
            self.label_photo6
        ]

        for label in labels:
            label.setStyleSheet("""
                QLabel {
                    border: 2px solid #C69C72;
                    background-color: #FFF9F3;
                    border-radius: 10px;
                }
            """)

        if selected_label is not None:
            selected_label.setStyleSheet("""
                QLabel {
                    border: 3px solid #8B5A2B;
                    background-color: #FFF9F3;
                    border-radius: 10px;
                }
            """)

    def addPhoto(self, event=None):
        album = self.comboBoxAlb.currentText()
        album_path = os.path.join(self.gallery_folder, album)

        if not album:
            QMessageBox.warning(self, "Warning", "Please select an album first")
            return

        if not os.path.exists(album_path):
            os.makedirs(album_path, exist_ok=True)

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

        shutil.copy2(file, new_path)

        self.updateGalleryJson(album, name)
        self.loadGallery()

    def deletePhoto(self):
        if not self.selected_photo:
            QMessageBox.warning(self, "Warning", "Please select photo first")
            return

        if os.path.exists(self.selected_photo):
            album = os.path.basename(os.path.dirname(self.selected_photo))
            image_name = os.path.basename(self.selected_photo)

            os.remove(self.selected_photo)
            self.removePhotoFromGalleryJson(album, image_name)

        self.selected_photo = None
        self.loadGallery()

    def updateGalleryJson(self, album, image):
        if not os.path.exists(self.gallery_json):
            data = {"albums": []}
        else:
            with open(self.gallery_json, encoding="utf8") as f:
                data = json.load(f)

        if "albums" not in data or not isinstance(data["albums"], list):
            data["albums"] = []

        found = False
        for alb in data["albums"]:
            if alb.get("name", "").lower() == album.lower():
                if "images" not in alb or not isinstance(alb["images"], list):
                    alb["images"] = []
                item = f"{album}/{image}"
                if item not in alb["images"]:
                    alb["images"].append(item)
                found = True
                break

        if not found:
            data["albums"].append({
                "name": album,
                "images": [f"{album}/{image}"]
            })

        with open(self.gallery_json, "w", encoding="utf8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def removePhotoFromGalleryJson(self, album, image):
        if not os.path.exists(self.gallery_json):
            return

        with open(self.gallery_json, encoding="utf8") as f:
            data = json.load(f)

        for alb in data.get("albums", []):
            if alb.get("name", "").lower() == album.lower():
                item = f"{album}/{image}"
                if item in alb.get("images", []):
                    alb["images"].remove(item)
                break

        with open(self.gallery_json, "w", encoding="utf8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def loadReviews(self):
        if not os.path.exists(self.review_path):
            self.reviews = []
            self.displayReviews([])
            return

        with open(self.review_path, encoding="utf8") as f:
            data = json.load(f)

        if isinstance(data, list):
            self.reviews = data
        else:
            self.reviews = data.get("reviews", [])

        self.displayReviews(self.reviews)

    def displayReviews(self, reviews):
        layout = self.verticalLayout_5

        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            widget = item.widget() if item else None
            if widget:
                widget.deleteLater()

        for review in reviews:
            frame = QFrame()
            frame.setStyleSheet("""
                QFrame {
                    border: 2px solid #C69C72;
                    background-color: #FFF9F3;
                    border-radius: 20px;
                    padding: 10px;
                }
            """)

            stars = "⭐" * review.get("rating", 0)

            text = (
                f"<div style='color:#6B3F1D; line-height:1.5;'>"
                f"<div style='font-size:15px; font-weight:700;'>Name: {review.get('name', '')}</div>"
                f"<div style='font-size:13px; color:#8A6A4A;'>Email: {review.get('email', '')}</div>"
                f"<div style='font-size:14px; margin-top:6px;'>Rating: {stars}</div>"
                f"<div style='font-size:14px; margin-top:10px; font-weight:600;'>Review:</div>"
                f"<div style='font-size:14px; color:#6B3F1D;'>{review.get('review', '')}</div>"
                f"</div>"
            )

            label = QLabel(text)
            label.setWordWrap(True)
            label.setTextFormat(Qt.TextFormat.RichText)
            label.setStyleSheet("""
                QLabel {
                    color: #6B3F1D;
                    background: transparent;
                    border: none;
                    font-size: 14px;
                    padding: 8px;
                }
            """)

            layout_card = QVBoxLayout(frame)
            layout_card.setContentsMargins(16, 16, 16, 16)
            layout_card.addWidget(label)

            frame.mousePressEvent = lambda e, r=review: self.selectReview(r)
            layout.addWidget(frame)

    def selectReview(self, review):
        self.selected_review = review

    def filterReviews(self):
        text = self.comboBoxRating.currentText()

        if text == "View All":
            filtered = self.reviews
        else:
            stars = int(text[0])
            filtered = [r for r in self.reviews if r.get("rating", 0) == stars]

        self.displayReviews(filtered)

    def deleteReview(self):
        if not self.selected_review:
            QMessageBox.warning(self, "Warning", "Select review first")
            return

        if not os.path.exists(self.review_path):
            return

        with open(self.review_path, encoding="utf8") as f:
            data = json.load(f)

        reviews = data.get("reviews", []) if isinstance(data, dict) else data
        reviews = [r for r in reviews if r != self.selected_review]

        if isinstance(data, dict):
            data["reviews"] = reviews
        else:
            data = reviews

        with open(self.review_path, "w", encoding="utf8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        self.selected_review = None
        self.loadReviews()

    def goBack(self):
        self.home = AdminHomeMainWindowEx()
        self.home.show()
        self.close()