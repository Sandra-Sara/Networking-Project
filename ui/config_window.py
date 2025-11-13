"""
Server configuration window for CryptPort
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QMessageBox, QFormLayout, QFrame
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont


class ConfigWindow(QWidget):
    """Server configuration setup window"""

    config_complete = pyqtSignal(dict)  # Emits server configuration

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Server Configuration - CryptPort")
        self.setFixedSize(1400, 700)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(20)

        # --- Title ---
        title = QLabel("⚙️ Server Configuration")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # --- Box around input fields ---
        box = QFrame()
        box.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                border: 2px solid #BBDEFB;
            }
        """)
        box_layout = QVBoxLayout(box)
        box_layout.setContentsMargins(80, 60, 80, 60)
        box_layout.setSpacing(30)

        form = QFormLayout()
        form.setSpacing(25)
        label_font = QFont("Segoe UI", 14, QFont.Bold)
        input_font = QFont("Segoe UI", 13)

        # --- Input Fields (Wider fields) ---
        self.server_ip = QLineEdit()
        self.server_ip.setPlaceholderText("Enter Server IP (e.g., 192.168.1.5)")
        self.server_ip.setFont(input_font)
        self.server_ip.setMinimumWidth(500)
        self.server_ip.setStyleSheet("""
            QLineEdit {
                padding: 12px 14px;
                border-radius: 8px;
                border: 1.5px solid #90CAF9;
            }
            QLineEdit:focus {
                border: 2px solid #42A5F5;
            }
        """)

        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("Enter Port (e.g., 5000)")
        self.port_input.setFont(input_font)
        self.port_input.setMinimumWidth(500)
        self.port_input.setStyleSheet("""
            QLineEdit {
                padding: 12px 14px;
                border-radius: 8px;
                border: 1.5px solid #90CAF9;
            }
            QLineEdit:focus {
                border: 2px solid #42A5F5;
            }
        """)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter Username")
        self.username.setFont(input_font)
        self.username.setMinimumWidth(500)
        self.username.setStyleSheet("""
            QLineEdit {
                padding: 12px 14px;
                border-radius: 8px;
                border: 1.5px solid #90CAF9;
            }
            QLineEdit:focus {
                border: 2px solid #42A5F5;
            }
        """)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter Password")
        self.password.setEchoMode(QLineEdit.Password)
        self.password.setFont(input_font)
        self.password.setMinimumWidth(500)
        self.password.setStyleSheet("""
            QLineEdit {
                padding: 12px 14px;
                border-radius: 8px;
                border: 1.5px solid #90CAF9;
            }
            QLineEdit:focus {
                border: 2px solid #42A5F5;
            }
        """)

        # Add fields to form
        form.addRow(QLabel("🌐 Server IP:"), self.server_ip)
        form.addRow(QLabel("🔌 Port:"), self.port_input)
        form.addRow(QLabel("👤 Username:"), self.username)
        form.addRow(QLabel("🔑 Password:"), self.password)

        for i in range(form.rowCount()):
            label = form.itemAt(i, QFormLayout.LabelRole).widget()
            if label:
                label.setFont(label_font)

        box_layout.addLayout(form)

        # --- Save Button ---
        save_btn = QPushButton("💾 Save Configuration")
        save_btn.setFont(QFont("Segoe UI", 14, QFont.Bold))
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #42A5F5;
                color: white;
                border-radius: 10px;
                padding: 12px 36px;
            }
            QPushButton:hover {
                background-color: #1E88E5;
            }
        """)
        save_btn.clicked.connect(self.save_config)
        box_layout.addWidget(save_btn, alignment=Qt.AlignCenter)

        layout.addWidget(box, alignment=Qt.AlignCenter)
        self.setLayout(layout)

    # --- Logic ---
    def save_config(self):
        server_ip = self.server_ip.text().strip()
        port = self.port_input.text().strip()
        username = self.username.text().strip()
        password = self.password.text().strip()

        if not all([server_ip, port, username, password]):
            QMessageBox.warning(self, "Missing Info", "All fields are required!")
            return

        try:
            int(port)
        except ValueError:
            QMessageBox.warning(self, "Invalid Port", "Port must be a number.")
            return

        QMessageBox.information(self, "Success", "Configuration saved successfully!")

        config_data = {
            "server_ip": server_ip,
            "port": port,
            "username": username,
            "password": password
        }

        self.config_complete.emit(config_data)
