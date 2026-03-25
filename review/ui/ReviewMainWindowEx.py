import os
import json
from datetime import datetime

from PyQt6.QtWidgets import QMainWindow, QLabel, QMessageBox
from PyQt6.QtCore import Qt

from .ReviewMainWindow import Ui_MainWindow
from Lumora_Studio_Booking_System.utils_path import ensure_data_file


class ReviewMainWindowEx(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.setupUi(self)

        self.selected_rating = 0
        self.all_reviews = []

        self.file_path = ensure_data_file("datasets/reviews.json")

        self.setupBackButtonStyle()
        self.setupSignal()
        self.loadReviews()

    def setupBackButtonStyle(self):
        self.pushButtonBack.setText("Back")
        self.pushButtonBack.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            color: black;
            border: none;
            font-size: 15px;
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

    def setupSignal(self):
        self.pushButtonSubmit.clicked.connect(self.submitReview)
        self.pushButtonCancel.clicked.connect(self.clearForm)
        self.pushButtonBack.clicked.connect(self.goHome)

        self.pushButton1star.clicked.connect(lambda: self.setRating(1))
        self.pushButton2star.clicked.connect(lambda: self.setRating(2))
        self.pushButton3star.clicked.connect(lambda: self.setRating(3))
        self.pushButton4star.clicked.connect(lambda: self.setRating(4))
        self.pushButton5star.clicked.connect(lambda: self.setRating(5))

        self.pushButtonAll.clicked.connect(lambda: self.filterReview(0))
        self.pushButton1starFilter.clicked.connect(lambda: self.filterReview(1))
        self.pushButton2starFilter.clicked.connect(lambda: self.filterReview(2))
        self.pushButton3starFilter.clicked.connect(lambda: self.filterReview(3))
        self.pushButton4starFilter.clicked.connect(lambda: self.filterReview(4))
        self.pushButton5starFilter.clicked.connect(lambda: self.filterReview(5))

    def setRating(self, rating):
        self.selected_rating = rating

        stars = [
            self.pushButton1star,
            self.pushButton2star,
            self.pushButton3star,
            self.pushButton4star,
            self.pushButton5star
        ]

        for i, star in enumerate(stars):
            if i < rating:
                star.setStyleSheet("color:gold; font-size:22px; border:none;")
            else:
                star.setStyleSheet("color:gray; font-size:22px; border:none;")

    def submitReview(self):
        name = self.nameLineEdit_4.text().strip()
        email = self.emailLineEdit.text().strip()
        review_text = self.textEdit.toPlainText().strip()
        rating = self.selected_rating

        if name == "" or review_text == "" or rating == 0:
            QMessageBox.warning(
                self,
                "Warning",
                "Please fill name, review and rating"
            )
            return

        new_review = {
            "name": name,
            "email": email,
            "rating": rating,
            "review": review_text,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        if os.path.exists(self.file_path):
            with open(self.file_path, encoding="utf8") as f:
                data = json.load(f)
        else:
            data = {"reviews": []}

        if isinstance(data, list):
            data = {"reviews": data}

        if "reviews" not in data or not isinstance(data["reviews"], list):
            data["reviews"] = []

        data["reviews"].insert(0, new_review)

        with open(self.file_path, "w", encoding="utf8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        QMessageBox.information(self, "Success", "Thank you for your review!")

        self.clearForm()
        self.loadReviews()

    def clearForm(self):
        self.nameLineEdit_4.clear()
        self.emailLineEdit.clear()
        self.textEdit.clear()

        self.selected_rating = 0

        stars = [
            self.pushButton1star,
            self.pushButton2star,
            self.pushButton3star,
            self.pushButton4star,
            self.pushButton5star
        ]

        for star in stars:
            star.setStyleSheet("color:gray; font-size:22px; border:none;")

    def loadReviews(self):
        if not os.path.exists(self.file_path):
            self.all_reviews = []
            self.displayReviews([])
            return

        with open(self.file_path, encoding="utf8") as f:
            data = json.load(f)

        if isinstance(data, list):
            reviews = data
        else:
            reviews = data.get("reviews", [])

        self.all_reviews = reviews
        self.displayReviews(reviews)

    def filterReview(self, star):
        if star == 0:
            self.displayReviews(self.all_reviews)
            return

        filtered = []

        for r in self.all_reviews:
            if r.get("rating", 0) == star:
                filtered.append(r)

        self.displayReviews(filtered)

    def timeAgo(self, time_str):
        try:
            t = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        except Exception:
            return ""

        now = datetime.now()
        diff = now - t
        seconds = diff.total_seconds()

        if seconds < 60:
            return "just now"
        if seconds < 3600:
            return f"{int(seconds / 60)}m ago"
        if seconds < 86400:
            return f"{int(seconds / 3600)}h ago"
        if seconds < 604800:
            return f"{int(seconds / 86400)}d ago"

        return t.strftime("%d %b")

    def displayReviews(self, reviews):
        layout = self.verticalLayoutReviews

        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            widget = item.widget() if item else None
            if widget:
                widget.deleteLater()

        for r in reviews:
            rating = r.get("rating", 0)
            stars = "⭐" * rating

            name = r.get("name", "")
            email = r.get("email", "")
            review_text = r.get("review", "")
            created = r.get("created_at", "")

            time_ago = self.timeAgo(created)

            text = f"""
{stars}
{name} • {time_ago}
{email}

{review_text}
"""

            label = QLabel(text)
            label.setAlignment(Qt.AlignmentFlag.AlignLeft)
            label.setWordWrap(True)
            label.setStyleSheet("""
            border:2px solid #C9A27C;
            padding:18px;
            border-radius:12px;
            background:#FFF8F0;
            font-size:13px;
            """)

            layout.addWidget(label)

    def goHome(self):
        from Lumora_Studio_Booking_System.guest_ui.home.ui.HomeMainWindowEx import HomeMainWindowEx

        self.homeWindow = HomeMainWindowEx()
        self.homeWindow.show()
        self.close()