from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QHBoxLayout, QMessageBox, QFrame
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont

class ConfigWindow(QWidget):
    config_complete = pyqtSignal(dict)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Server Configuration")
        self.setStyleSheet("background-color: #f5f6fa;")
        self.setGeometry(300, 100, 800, 600)

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        # Outer card container
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 2px solid #dce3f0;
            }
        """)
        frame_layout = QVBoxLayout(frame)
        frame_layout.setContentsMargins(60, 40, 60, 40)
        frame_layout.setSpacing(20)

        # Title
        title_label = QLabel("⚙️ Server Configuration")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setFont(QFont("Arial", 20, QFont.Bold))
        frame_layout.addWidget(title_label)

        # Server IP
        self.ip_label, self.ip_input = self.create_input_row("🌐 Server IP:", "Enter Server IP (e.g., 192.168.1.5)")
        frame_layout.addLayout(self.ip_label)
        frame_layout.addWidget(self.ip_input)

        # Port
        self.port_label, self.port_input = self.create_input_row("🔌 Port:", "Enter Port (e.g., 5000)")
        frame_layout.addLayout(self.port_label)
        frame_layout.addWidget(self.port_input)

        # Username
        self.username_label, self.username_input = self.create_input_row("👤 Username:", "Enter Username")
        frame_layout.addLayout(self.username_label)
        frame_layout.addWidget(self.username_input)

        # Passkey (Updated)
        self.passkey_label, self.passkey_input = self.create_input_row("🔑 Passkey:", "Enter Passkey", is_password=True)
        frame_layout.addLayout(self.passkey_label)
        frame_layout.addWidget(self.passkey_input)

        # Save button
        self.save_button = QPushButton("💾 Save Configuration")
        self.save_button.setStyleSheet("""
            QPushButton {
                background-color: #409EFF;
                color: white;
                font-weight: bold;
                font-size: 16px;
                border-radius: 8px;
                padding: 10px 0;
            }
            QPushButton:hover {
                background-color: #66b1ff;
            }
        """)
        self.save_button.clicked.connect(self.save_config)
        frame_layout.addWidget(self.save_button, alignment=Qt.AlignCenter)

        main_layout.addWidget(frame, alignment=Qt.AlignCenter)

    def create_input_row(self, label_text, placeholder, is_password=False):
        layout = QHBoxLayout()
        label = QLabel(label_text)
        label.setFont(QFont("Arial", 12, QFont.Bold))
        label.setFixedWidth(130)
        label.setStyleSheet("color: #2f3640;")
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        input_field.setFont(QFont("Arial", 11))
        input_field.setFixedHeight(40)
        input_field.setMinimumWidth(400)
        input_field.setStyleSheet("""
            QLineEdit {
                border: 2px solid #d0d7de;
                border-radius: 6px;
                padding-left: 10px;
            }
            QLineEdit:focus {
                border: 2px solid #409EFF;
            }
        """)
        if is_password:
            input_field.setEchoMode(QLineEdit.Password)
        layout.addWidget(label)
        layout.addWidget(input_field)
        return layout, input_field

    def save_config(self):
        host = self.ip_input.text().strip()
        port = self.port_input.text().strip()
        username = self.username_input.text().strip()
        passkey = self.passkey_input.text().strip()

        if not host or not port or not username or not passkey:
            QMessageBox.warning(self, "Missing Fields", "Please fill in all fields before saving.")
            return

        config_data = {
            "host": host,
            "port": port,
            "username": username,
            "passkey": passkey
        }
        QMessageBox.information(self, "Saved", "Configuration saved successfully!")
        self.config_complete.emit(config_data)
