"""
Register window for new users (CryptPort)
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QLabel,
    QPushButton, QMessageBox, QHBoxLayout
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QIcon


class RegisterWindow(QWidget):
    # ✅ Signal emitted when registration succeeds
    register_success = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Register - cryptPort")
        self.setGeometry(100, 100,1700,700)  # Bigger window

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(15)

        # --- Fonts ---
        title_font = QFont("Segoe UI", 22, QFont.Bold)
        subtitle_font = QFont("Segoe UI", 12)
        input_font = QFont("Segoe UI", 12)
        button_font = QFont("Segoe UI", 13, QFont.Bold)

        # --- Title Section ---
        title_label = QLabel("Welcome to cryptPort")
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)

        subtitle_label = QLabel("A simple and reliable file transfer platform")
        subtitle_label.setFont(subtitle_font)
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: gray; font-weight: bold;")

        # --- Username Field with Icon ---
        username_layout = QHBoxLayout()
        username_icon = QLabel()
        username_icon.setPixmap(QIcon("assets/icons/user.png").pixmap(QSize(24, 24)))
        username_input = QLineEdit()
        username_input.setPlaceholderText("Username")
        username_input.setFont(input_font)
        username_layout.addWidget(username_icon)
        username_layout.addWidget(username_input)

        # --- Email Field with Icon ---
        email_layout = QHBoxLayout()
        email_icon = QLabel()
        email_icon.setPixmap(QIcon("assets/icons/email.png").pixmap(QSize(24, 24)))
        email_input = QLineEdit()
        email_input.setPlaceholderText("Email")
        email_input.setFont(input_font)
        email_layout.addWidget(email_icon)
        email_layout.addWidget(email_input)

        # --- Password Field with Icon ---
        password_layout = QHBoxLayout()
        password_icon = QLabel()
        password_icon.setPixmap(QIcon("assets/icons/lock.png").pixmap(QSize(24, 24)))
        password_input = QLineEdit()
        password_input.setPlaceholderText("Password")
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setFont(input_font)
        password_layout.addWidget(password_icon)
        password_layout.addWidget(password_input)

        # --- Confirm Password Field with Icon ---
        confirm_layout = QHBoxLayout()
        confirm_icon = QLabel()
        confirm_icon.setPixmap(QIcon("assets/icons/lock.png").pixmap(QSize(24, 24)))
        confirm_input = QLineEdit()
        confirm_input.setPlaceholderText("Confirm Password")
        confirm_input.setEchoMode(QLineEdit.Password)
        confirm_input.setFont(input_font)
        confirm_layout.addWidget(confirm_icon)
        confirm_layout.addWidget(confirm_input)

        # --- Register Button ---
        register_button = QPushButton("Register")
        register_button.setFont(button_font)
        register_button.setIcon(QIcon("assets/icons/register.png"))
        register_button.setIconSize(QSize(22, 22))
        register_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        register_button.clicked.connect(self.handle_register)

        # Assign inputs to self
        self.username_input = username_input
        self.email_input = email_input
        self.password_input = password_input
        self.confirm_input = confirm_input
        self.register_button = register_button

        # --- Add Widgets to Layout ---
        layout.addWidget(title_label)
        layout.addWidget(subtitle_label)
        layout.addSpacing(15)
        layout.addLayout(username_layout)
        layout.addLayout(email_layout)
        layout.addLayout(password_layout)
        layout.addLayout(confirm_layout)
        layout.addWidget(register_button)

        self.setLayout(layout)

    def handle_register(self):
        """Validate registration inputs"""
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        confirm = self.confirm_input.text().strip()

        if not username or not email or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return

        if password != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return

        if len(password) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters")
            return

        # ✅ Registration success
        QMessageBox.information(
            self,
            "Registration Successful",
            "Account created successfully!\nPlease login to continue."
        )

        # Emit success signal and close window
        self.register_success.emit()
        self.close()
