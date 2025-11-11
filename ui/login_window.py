"""
Login window for user authentication (CryptPort)
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QSpacerItem, QSizePolicy
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal, QSize


class LoginWindow(QWidget):
    """Login window for existing users"""

    login_success = pyqtSignal(str)  # emits email after login
    go_register = pyqtSignal()       # emits when user clicks "Register"

    def __init__(self, prefill_email: str = ""):
        super().__init__()
        self.prefill_email = prefill_email
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login - CryptPort")
        self.setGeometry(100, 100, 700, 500)
        self.setStyleSheet("background-color: #f8fafc;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        # --- Fonts ---
        title_font = QFont("Segoe UI", 20, QFont.Bold)
        label_font = QFont("Segoe UI", 12)
        button_font = QFont("Segoe UI", 13, QFont.Bold)

        # --- App Branding ---
        title_label = QLabel("Welcome Back to CryptPort")
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)

        subtitle_label = QLabel("A simple and reliable file transfer platform")
        subtitle_label.setFont(QFont("Segoe UI", 11))
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: gray;")

        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)

        layout.addSpacerItem(QSpacerItem(20, 30, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # --- Email ---
        email_layout = QHBoxLayout()
        email_icon = QLabel()
        email_pixmap = QPixmap("assets/icons/email.png")
        email_icon.setPixmap(email_pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        email_layout.addWidget(email_icon)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.email_input.setText(self.prefill_email)
        self.email_input.setFont(label_font)
        email_layout.addWidget(self.email_input)
        layout.addLayout(email_layout)

        # --- Password ---
        pass_layout = QHBoxLayout()
        pass_icon = QLabel()
        pass_pixmap = QPixmap("assets/icons/lock.png")
        pass_icon.setPixmap(pass_pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        pass_layout.addWidget(pass_icon)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setFont(label_font)
        pass_layout.addWidget(self.password_input)
        layout.addLayout(pass_layout)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        # --- Buttons ---
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        self.login_button = QPushButton("Login")
        self.login_button.setFont(button_font)
        self.login_button.setIcon(QIcon("assets/icons/login.png"))
        self.login_button.setIconSize(QSize(20, 20))
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px 28px;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #45a049; }
        """)
        self.login_button.clicked.connect(self.login_user)

        self.register_button = QPushButton("Register")
        self.register_button.setFont(button_font)
        self.register_button.setIcon(QIcon("assets/icons/user-add.png"))
        self.register_button.setIconSize(QSize(20, 20))
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                padding: 10px 28px;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #0063B1; }
        """)
        self.register_button.clicked.connect(self.go_register.emit)

        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.register_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def login_user(self):
        """Handle login (no backend, just local validation)"""
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Missing Info", "Please enter both email and password.")
            return

        if "@" not in email or len(password) < 3:
            QMessageBox.critical(self, "Login Failed", "Invalid email or password.")
            return

        # ✅ Simulate successful login
        QMessageBox.information(self, "Login Successful", f"Welcome back, {email}!")
        self.login_success.emit(email)
        self.close()
