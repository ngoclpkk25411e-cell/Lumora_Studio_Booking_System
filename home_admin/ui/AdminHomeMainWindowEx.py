import os

from PyQt6.QtWidgets import QWidget, QLabel, QPushButton
from PyQt6.QtGui import QIcon, QPixmap, QFont
from PyQt6.QtCore import QSize, Qt

from .AdminHomeMainWindow import Ui_Form


class AdminHomeMainWindowEx(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.base_dir = os.path.dirname(
            os.path.dirname(
                os.path.dirname(
                    os.path.dirname(__file__)
                )
            )
        )

        self.icon_folder = os.path.join(self.base_dir, "assets", "icons")

        self.applyModernStyle()
        self.setupIcons()
        self.setupCardImages()
        self.setupSignal()

    def applyModernStyle(self):
        self.setStyleSheet("""
        QWidget {
            background-color: #F7F1EA;
            color: #6B3F1D;
            font-family: "Times New Roman";
            font-size: 15px;
        }

        QLabel {
            color: #6B3F1D;
            background: transparent;
            border: none;
        }

        QPushButton {
            background-color: #F3E7D8;
            color: #7A4A22;
            border: 1.5px solid #C69C72;
            border-radius: 16px;
            padding: 8px 12px;
            font-size: 15px;
            font-weight: 700;
            text-align: left;
        }

        QPushButton:hover {
            background-color: #EBD9C3;
        }

        QPushButton:pressed {
            background-color: #DFC9B1;
        }

        #pushButtonLogOut {
            background-color: #EFD2B7;
            font-size: 17px;
            text-align: center;
        }

        #pushButtonDashBoard, #pushButtonAppointments, #pushButtonCustomers, #pushButtonGallery {
            background: transparent;
            border: none;
            color: #6B3F1D;
            font-size: 16px;
            font-weight: 700;
            padding: 10px 8px;
        }

        #pushButtonDashBoard:hover, #pushButtonAppointments:hover,
        #pushButtonCustomers:hover, #pushButtonGallery:hover {
            background-color: rgba(239, 210, 183, 0.65);
            border-radius: 12px;
        }
        """)

        # Làm chữ rõ hơn cho toàn bộ label tiêu đề/chú thích
        for lb in self.findChildren(QLabel):
            txt = lb.text().strip().lower()
            if "hello admin" in txt:
                f = QFont("Times New Roman", 30)
                f.setBold(True)
                lb.setFont(f)
                lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
                lb.setStyleSheet("color:#6B3F1D; background:transparent; border:none;")
            elif "choose" in txt:
                f = QFont("Times New Roman", 18)
                lb.setFont(f)
                lb.setAlignment(Qt.AlignmentFlag.AlignCenter)
                lb.setStyleSheet("color:#B57E45; background:transparent; border:none;")
            elif "dashboard" in txt or "customer" in txt or "schedule" in txt or "content" in txt:
                f = QFont("Times New Roman", 24)
                f.setBold(True)
                lb.setFont(f)
                lb.setStyleSheet("color:#7A4A22; background:transparent; border:none;")
            elif "system overview" in txt or "manage customer" in txt or "manage appointment" in txt or "manage gallery" in txt:
                f = QFont("Times New Roman", 16)
                lb.setFont(f)
                lb.setWordWrap(True)
                lb.setStyleSheet("color:#B57E45; background:transparent; border:none;")

    def setupIcons(self):
        dashboard_icon = os.path.join(self.icon_folder, "dashboard.png")
        schedule_icon = os.path.join(self.icon_folder, "schedule.png")
        customer_icon = os.path.join(self.icon_folder, "customer.png")
        content_icon = os.path.join(self.icon_folder, "content.png")

        # sidebar
        if os.path.exists(dashboard_icon) and hasattr(self, "pushButtonDashBoard"):
            self.pushButtonDashBoard.setIcon(QIcon(dashboard_icon))
            self.pushButtonDashBoard.setIconSize(QSize(28, 28))

        if os.path.exists(schedule_icon) and hasattr(self, "pushButtonAppointments"):
            self.pushButtonAppointments.setIcon(QIcon(schedule_icon))
            self.pushButtonAppointments.setIconSize(QSize(28, 28))

        if os.path.exists(customer_icon) and hasattr(self, "pushButtonCustomers"):
            self.pushButtonCustomers.setIcon(QIcon(customer_icon))
            self.pushButtonCustomers.setIconSize(QSize(28, 28))

        if os.path.exists(content_icon) and hasattr(self, "pushButtonGallery"):
            self.pushButtonGallery.setIcon(QIcon(content_icon))
            self.pushButtonGallery.setIconSize(QSize(28, 28))

    def setupCardImages(self):
        # file hiện tại trước đây chỉ gắn icon cho menu trái, nên các ô hình ở giữa bị trống. fileciteturn13file0
        image_map = {
            "dashboard": os.path.join(self.icon_folder, "dashboard.png"),
            "customer": os.path.join(self.icon_folder, "customer.png"),
            "schedule": os.path.join(self.icon_folder, "schedule.png"),
            "content": os.path.join(self.icon_folder, "content.png"),
        }

        # thử gắn ảnh vào các label/placeholder hay gặp trong UI
        candidate_map = {
            "dashboard": ["labelDashboardIcon", "labelDashBoardIcon", "label_9", "label_dashboard"],
            "customer": ["labelCustomerIcon", "label_customer", "label_10"],
            "schedule": ["labelScheduleIcon", "labelAppointmentsIcon", "label_schedule", "label_11"],
            "content": ["labelContentIcon", "labelGalleryIcon", "label_content", "label_12"],
        }

        for key, names in candidate_map.items():
            img = image_map[key]
            if not os.path.exists(img):
                continue
            for name in names:
                w = getattr(self, name, None)
                if isinstance(w, QLabel):
                    pix = QPixmap(img).scaled(
                        110, 110,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation
                    )
                    w.setPixmap(pix)
                    w.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    w.setStyleSheet("""
                        QLabel {
                            background-color: #F7F1EA;
                            border: 1.5px solid #D2B08A;
                            border-radius: 18px;
                        }
                    """)

        # Nếu card dưới là QPushButton trống, gắn icon trực tiếp vào button
        button_candidates = {
            "dashboard": ["pushButtonDashboardCard", "pushButtonDashBoardCard", "pushButton_9"],
            "customer": ["pushButtonCustomerCard", "pushButton_10"],
            "schedule": ["pushButtonScheduleCard", "pushButtonAppointmentCard", "pushButton_11"],
            "content": ["pushButtonContentCard", "pushButtonGalleryCard", "pushButton_12"],
        }

        for key, names in button_candidates.items():
            img = image_map[key]
            if not os.path.exists(img):
                continue
            for name in names:
                w = getattr(self, name, None)
                if isinstance(w, QPushButton):
                    w.setIcon(QIcon(img))
                    w.setIconSize(QSize(96, 96))
                    w.setStyleSheet("""
                        QPushButton {
                            background-color: #F7F1EA;
                            border: 1.5px solid #D2B08A;
                            border-radius: 18px;
                        }
                        QPushButton:hover {
                            background-color: #F1E3D2;
                        }
                    """)

    def setupSignal(self):
        self.pushButtonDashBoard.clicked.connect(self.openDashboard)
        self.pushButtonAppointments.clicked.connect(self.openAppointments)
        self.pushButtonCustomers.clicked.connect(self.openCustomers)
        self.pushButtonGallery.clicked.connect(self.openContent)
        self.pushButtonLogOut.clicked.connect(self.process_logout)

    def openDashboard(self):
        from ...dashboard.ui.DashBoardMainWindowEx import DashBoardMainWindowEx
        self.dashboardWindow = DashBoardMainWindowEx()
        if hasattr(self.dashboardWindow, "showWindow"):
            self.dashboardWindow.showWindow()
        else:
            self.dashboardWindow.show()
        self.close()

    def openAppointments(self):
        from ...managing_booking.ui.AppointmentMainWindowEx import AppointmentMainWindowEx
        self.appointmentWindow = AppointmentMainWindowEx()
        self.appointmentWindow.show()
        self.close()

    def openCustomers(self):
        from ...cus_information.ui.CustomerMainWindowEx import CustomerMainWindowEx
        self.customerWindow = CustomerMainWindowEx()
        self.customerWindow.show()
        self.close()

    def openContent(self):
        from ...content.ui.ContentMainWindowEx import ContentMainWindowEx
        self.contentWindow = ContentMainWindowEx()
        self.contentWindow.show()
        self.close()

    def process_logout(self):
        from ...login.ui.LoginMainWindowEx import LoginMainWindowEx
        self.loginWindow = LoginMainWindowEx()
        self.loginWindow.show()
        self.close()
