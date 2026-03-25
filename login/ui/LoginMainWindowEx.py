import os
import sys

from PyQt6.QtWidgets import QMessageBox, QLineEdit, QMainWindow
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QSize

from .LoginMainWindow import Ui_LoginMainWindow
from Lumora_Studio_Booking_System.utils_path import resource_path


# import an toàn hơn để tránh lỗi khi chạy test / chạy trực tiếp / đóng gói
from Lumora_Studio_Booking_System.admin_ui.home_admin.ui.AdminHomeMainWindowEx import AdminHomeMainWindowEx



class LoginMainWindowEx(QMainWindow, Ui_LoginMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.adminHome = None
        self.home = None

        self.setup_safe()
        self.setupImages()
        self.setupStyles()
        self.setupSignals()

    def setup_safe(self):
        if hasattr(self, "lineEditPassword") and self.lineEditPassword:
            self.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Password)

    def setupSignals(self):
        if hasattr(self, "pushButtonLogin") and self.pushButtonLogin:
            self.pushButtonLogin.clicked.connect(self.process_login)

        if hasattr(self, "pushButtonBack") and self.pushButtonBack:
            self.pushButtonBack.clicked.connect(self.goHome)

    def get_image_path(self, filename):
        image_dir = resource_path("admin_ui/login/images")
        path = os.path.join(image_dir, filename)
        return path if os.path.exists(path) else None

    def set_pixmap(self, widget, path, keep_ratio=True):
        if widget is None or not path or not os.path.exists(path):
            return

        pix = QPixmap(path)
        if pix.isNull():
            return

        width = max(widget.width(), 40)
        height = max(widget.height(), 40)

        if keep_ratio:
            pix = pix.scaled(
                width,
                height,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
        else:
            pix = pix.scaled(
                width,
                height,
                Qt.AspectRatioMode.IgnoreAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

        widget.setPixmap(pix)
        widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def setupImages(self):
        path_user = self.get_image_path("ic_2.png")
        path_lock = self.get_image_path("ic_1.png")
        path_back = self.get_image_path("left_arrow.png")
        path_login = self.get_image_path("ic_login.png")
        path_thumb = self.get_image_path("thumnail.png")
        path_subject = self.get_image_path("Subject.png")
        path_star = self.get_image_path("ic_star.png")
        path_shining = self.get_image_path("ic_shining.png")

        self.set_pixmap(getattr(self, "label_3", None), path_user)
        self.set_pixmap(getattr(self, "label_4", None), path_lock)
        self.set_pixmap(getattr(self, "label", None), path_thumb, keep_ratio=False)
        self.set_pixmap(getattr(self, "label_7", None), path_subject)
        self.set_pixmap(getattr(self, "label_11", None), path_star)
        self.set_pixmap(getattr(self, "label_9", None), path_shining)

        if hasattr(self, "pushButtonBack") and self.pushButtonBack and path_back:
            self.pushButtonBack.setIcon(QIcon(path_back))
            self.pushButtonBack.setIconSize(QSize(20, 20))
            self.pushButtonBack.setText("")

        if hasattr(self, "pushButtonLogin") and self.pushButtonLogin and path_login:
            self.pushButtonLogin.setIcon(QIcon(path_login))
            self.pushButtonLogin.setIconSize(QSize(22, 22))

    def setupStyles(self):
        self.setStyleSheet("""
        QMainWindow, QWidget {
            background-color: #F7F1EA;
            color: #6B3F1D;
            font-family: "Times New Roman";
            font-size: 14px;
        }

        QLabel {
            color: #6B3F1D;
            background: transparent;
            border: none;
        }

        QLineEdit {
            background-color: #FFF9F3;
            color: #6B3F1D;
            border: 1.5px solid #D5B79A;
            border-radius: 18px;
            padding: 10px 16px;
            font-size: 14px;
        }

        QLineEdit::placeholder {
            color: #B8A08A;
        }

        QPushButton {
            background-color: #8E6B49;
            color: white;
            border: none;
            border-radius: 18px;
            padding: 10px 18px;
            font-size: 15px;
            font-weight: 700;
        }

        QPushButton:hover {
            background-color: #7C5B3D;
        }

        QPushButton:pressed {
            background-color: #6B4A2D;
        }
        """)

        if hasattr(self, "pushButtonBack") and self.pushButtonBack:
            self.pushButtonBack.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #8B5A2B;
                border: none;
                font-size: 16px;
                font-weight: 700;
                text-align: left;
                padding: 4px 6px;
            }
            QPushButton:hover {
                color: #6B3F1D;
                text-decoration: underline;
                background: transparent;
            }
            """)

        if hasattr(self, "label_2") and self.label_2:
            self.label_2.setStyleSheet("""
            QLabel {
                color: #8B6A4A;
                background: transparent;
                border: none;
                font-family: "Times New Roman";
                font-size: 42px;
                font-weight: 700;
            }
            """)

        for name in ["label_3", "label_4"]:
            widget = getattr(self, name, None)
            if widget:
                widget.setStyleSheet("""
                QLabel {
                    background: transparent;
                    border: none;
                }
                """)

    def process_login(self):
        if not hasattr(self, "lineEditUser") or not hasattr(self, "lineEditPassword"):
            QMessageBox.critical(self, "Error", "Thiếu lineEditUser hoặc lineEditPassword trong UI.")
            return

        username = self.lineEditUser.text().strip()
        password = self.lineEditPassword.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Warning", "Vui lòng nhập đầy đủ tài khoản và mật khẩu!")
            return

        if username == "hellolumora@gmail.com" and password == "123456":
            if AdminHomeMainWindowEx is None:
                QMessageBox.critical(
                    self,
                    "Import Error",
                    "Không import được AdminHomeMainWindowEx. Hãy kiểm tra lại đường dẫn module."
                )
                return

            QMessageBox.information(self, "Success", "Login successful!")
            self.adminHome = AdminHomeMainWindowEx()
            self.adminHome.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Sai tài khoản hoặc mật khẩu!")

    def goHome(self):
        try:
            from Lumora_Studio_Booking_System.guest_ui.home.ui.HomeMainWindowEx import HomeMainWindowEx
            self.home = HomeMainWindowEx()
            self.home.show()
            self.close()
        except Exception as e:
            QMessageBox.critical(self, "Import Error", f"Không mở được Home: {str(e)}")


if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = LoginMainWindowEx()
    window.show()
    sys.exit(app.exec())