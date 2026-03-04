from PyQt6.QtWidgets import QMessageBox, QLineEdit, QMainWindow

from ui.LoginMainWindow import Ui_LoginMainWindow


class LoginMainWindowEx(QMainWindow,Ui_LoginMainWindow):
    def __init__(self):
        super().__init__()
        # GỌI setupUi Ở ĐÂY
        self.setupUi(self)
        # Ẩn password
        self.lineEditPassword.setEchoMode(QLineEdit.EchoMode.Password)
        # Bắt sự kiện login
        self.pushButtonLogin.clicked.connect(self.process_login)
    def process_login(self):
        username = self.lineEditUser.text()
        password = self.lineEditPassword.text()

        if username == "KhanhNgoc@123" and password == "123456":
            QMessageBox.information(self, "Success", "Login successful!")
        else:
            QMessageBox.warning(self, "Error", "Sai tài khoản hoặc mật khẩu!")