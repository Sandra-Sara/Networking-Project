from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class ConnectionTab(QWidget):
    connection_requested = pyqtSignal(str, str, str, str)
    disconnection_requested = pyqtSignal()

    def __init__(self, config_data=None):
        super().__init__()
        self.config_data = config_data or {}

        self.setStyleSheet("background-color: #f5f6fa;")

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        # Outer card
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
        title_label = QLabel("🌐 Connect to Server")
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

        # Pre-fill from saved config
        self.load_config_data()

        # Buttons
        btn_layout = QHBoxLayout()
        self.connect_button = QPushButton("🔗 Connect")
        self.disconnect_button = QPushButton("❌ Disconnect")

        for btn, color in [(self.connect_button, "#409EFF"), (self.disconnect_button, "#e74c3c")]:
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {color};
                    color: white;
                    font-weight: bold;
                    font-size: 16px;
                    border-radius: 8px;
                    padding: 10px 0;
                    min-width: 150px;
                }}
                QPushButton:hover {{
                    background-color: #66b1ff;
                }}
            """)

        self.connect_button.clicked.connect(self.handle_connect)
        self.disconnect_button.clicked.connect(self.handle_disconnect)

        btn_layout.addWidget(self.connect_button)
        btn_layout.addWidget(self.disconnect_button)
        frame_layout.addLayout(btn_layout)

        # Connection status
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Arial", 12))
        frame_layout.addWidget(self.status_label)

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

    def load_config_data(self):
        self.ip_input.setText(self.config_data.get("host", ""))
        self.port_input.setText(self.config_data.get("port", ""))
        self.username_input.setText(self.config_data.get("username", ""))
        self.passkey_input.setText(self.config_data.get("passkey", ""))

    def handle_connect(self):
        host = self.ip_input.text().strip()
        port = self.port_input.text().strip()
        username = self.username_input.text().strip()
        passkey = self.passkey_input.text().strip()

        if not host or not port or not username or not passkey:
            QMessageBox.warning(self, "Missing Fields", "Please fill in all fields before connecting.")
            return

        self.connection_requested.emit(host, port, username, passkey)

    def handle_disconnect(self):
        self.disconnection_requested.emit()

    def update_connection_status(self, connected, message):
        self.status_label.setText(message)
        self.status_label.setStyleSheet(
            "color: green;" if connected else "color: red;"
        )
