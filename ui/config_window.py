"""
Server configuration window for CryptPort
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QFormLayout
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont


class ConfigWindow(QWidget):
    """Server configuration setup window"""

    config_complete = pyqtSignal(dict)  # Emits server configuration when done

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Server Configuration - CryptPort")
        self.setFixedSize(900,700)
        self.init_ui()

    def init_ui(self):
        """Setup configuration UI"""
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(15)

        title = QLabel("Server Configuration")
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        form = QFormLayout()

        self.server_ip = QLineEdit()
        self.server_ip.setPlaceholderText("Enter Server IP (e.g., 192.168.1.5)")
        form.addRow("Server IP:", self.server_ip)

        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("Enter Port (e.g., 5000)")
        form.addRow("Port:", self.port_input)

        self.username = QLineEdit()
        self.username.setPlaceholderText("Enter Username")
        form.addRow("Username:", self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Enter Password")
        self.password.setEchoMode(QLineEdit.Password)
        form.addRow("Password:", self.password)

        layout.addLayout(form)

        # Save Button
        save_btn = QPushButton("Save Configuration")
        save_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 8px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        save_btn.clicked.connect(self.save_config)
        layout.addWidget(save_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def save_config(self):
        """Validate and emit configuration"""
        server_ip = self.server_ip.text().strip()
        port = self.port_input.text().strip()
        username = self.username.text().strip()
        password = self.password.text().strip()

        if not server_ip or not port or not username or not password:
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
        self.close()
