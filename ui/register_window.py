"""
Register window for new users (CryptPort)
Styled consistently with Server Configuration page
Uses built-in emoji icons (no external image assets)
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton,
    QMessageBox, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette


class RegisterWindow(QWidget):
    register_success = pyqtSignal()  # ✅ Emits when registration succeeds

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Setup the consistent UI"""
        self.setWindowTitle("Register - CryptPort")
        self.setGeometry(200, 100, 1000, 700)

        # Background color (soft blue like Config Page)
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#E3F2FD"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # --- Main Layout ---
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(30)

        # --- Title ---
        title = QLabel("🧩 Create Your CryptPort Account")
        title.setFont(QFont("Segoe UI", 26, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Secure file sharing starts here")
        subtitle.setFont(QFont("Segoe UI", 13))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: gray; font-weight: 500;")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # --- Centered White Box ---
        box = QFrame()
        box.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 18px;
                border: 2px solid #BBDEFB;
            }
        """)
        box.setFixedWidth(550)
        box_layout = QVBoxLayout(box)
        box_layout.setContentsMargins(60, 50, 60, 50)
        box_layout.setSpacing(22)

        input_font = QFont("Segoe UI", 12)
        label_font = QFont("Segoe UI", 13, QFont.Bold)

        # ✅ Helper to create consistent input rows
        def create_input_row(label_text, placeholder, echo=False):
            layout = QHBoxLayout()
            layout.setSpacing(15)

            label = QLabel(label_text)
            label.setFont(label_font)
            label.setAlignment(Qt.AlignRight)

            field = QLineEdit()
            field.setPlaceholderText(placeholder)
            field.setFont(input_font)
            field.setStyleSheet("""
                QLineEdit {
                    border: 1.5px solid #90CAF9;
                    border-radius: 10px;
                    padding: 10px 12px;
                    background-color: #FAFAFA;
                }
                QLineEdit:focus {
                    border: 2px solid #42A5F5;
                    background-color: white;
                }
            """)
            if echo:
                field.setEchoMode(QLineEdit.Password)

            layout.addWidget(label)
            layout.addWidget(field)
            return layout, field

        # --- Input Fields (with emoji icons) ---
        user_layout, self.username_input = create_input_row("👤 Username:", "Enter your username")
        email_layout, self.email_input = create_input_row("✉️ Email:", "Enter your email address")
        pass_layout, self.password_input = create_input_row("🔒 Password:", "Enter password", echo=True)
        confirm_layout, self.confirm_input = create_input_row("🔑 Confirm:", "Confirm password", echo=True)

        # --- Register Button ---
        self.register_button = QPushButton("Create Account")
        self.register_button.setFont(QFont("Segoe UI", 14, QFont.Bold))
        self.register_button.setCursor(Qt.PointingHandCursor)
        self.register_button.setStyleSheet("""
            QPushButton {
                background-color: #42A5F5;
                color: white;
                border-radius: 12px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #1E88E5;
            }
            QPushButton:pressed {
                background-color: #1565C0;
            }
        """)
        self.register_button.clicked.connect(self.handle_register)

        # --- Add All Widgets to Box ---
        box_layout.addLayout(user_layout)
        box_layout.addLayout(email_layout)
        box_layout.addLayout(pass_layout)
        box_layout.addLayout(confirm_layout)
        box_layout.addSpacing(10)
        box_layout.addWidget(self.register_button, alignment=Qt.AlignCenter)

        # Add box to main layout
        main_layout.addWidget(box, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    # =============================
    # ✅ Registration Logic
    # =============================
    def handle_register(self):
        username = self.username_input.text().strip()
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        confirm = self.confirm_input.text().strip()

        if not username or not email or not password or not confirm:
            QMessageBox.warning(self, "Error", "Please fill in all fields")
            return

        if password != confirm:
            QMessageBox.warning(self, "Error", "Passwords do not match")
            return

        if len(password) < 6:
            QMessageBox.warning(self, "Error", "Password must be at least 6 characters long")
            return

        # ✅ Registration success
        QMessageBox.information(
            self,
            "Registration Successful",
            "Your account has been created successfully!\nPlease login to continue."
        )
        self.register_success.emit()
        self.close()
