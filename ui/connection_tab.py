"""
ConnectionTab (CryptPort)
Beautifully styled connection window that links with main.py and file_tab.py
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit,
    QMessageBox, QHBoxLayout, QFrame, QFormLayout
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QPalette


class ConnectionTab(QWidget):
    """Connection interface after server configuration"""

    # ✅ Signals to communicate with main.py
    connection_requested = pyqtSignal(str, int, str, str)
    disconnection_requested = pyqtSignal()

    def __init__(self, config_data=None):  # ✅ Fixed: double underscores
        super().__init__()
        self.config_data = config_data or {}
        self.connected = False
        self.init_ui()

    def init_ui(self):
        """Setup UI"""
        self.setWindowTitle("Server Connection - CryptPort")
        self.setFixedSize(950, 720)

        # Light blue background
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#E3F2FD"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # --- Main layout ---
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(25)

        # --- Title ---
        title = QLabel("🔗 Connect to CryptPort Server")
        title.setFont(QFont("Segoe UI", 26, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Enter your server credentials to begin your secure session ⚡")
        subtitle.setFont(QFont("Segoe UI", 13))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: gray; font-weight: 500;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # --- Connection Box ---
        box = QFrame()
        box.setFixedWidth(520)
        box.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 16px;
                border: 2px solid #BBDEFB;
            }
        """)

        form_layout = QFormLayout(box)
        form_layout.setContentsMargins(60, 50, 60, 50)
        form_layout.setSpacing(20)

        input_font = QFont("Segoe UI", 12)

        # --- Input Fields ---
        self.server_input = QLineEdit()
        self.server_input.setPlaceholderText("Server IP Address")
        self._style_input(self.server_input, input_font)

        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("Port (e.g. 8080)")
        self._style_input(self.port_input, input_font)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self._style_input(self.username_input, input_font)

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self._style_input(self.password_input, input_font)

        form_layout.addRow("🌐 Server IP:", self.server_input)
        form_layout.addRow("⚙ Port:", self.port_input)
        form_layout.addRow("👤 Username:", self.username_input)
        form_layout.addRow("🔑 Password:", self.password_input)

        # --- Connection Buttons ---
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)

        self.connect_btn = QPushButton("Connect to Server")
        self.disconnect_btn = QPushButton("Disconnect")

        self._style_button(self.connect_btn, "#42A5F5", "#1E88E5", "#1565C0")
        self._style_button(self.disconnect_btn, "#E53935", "#D32F2F", "#B71C1C")

        self.connect_btn.clicked.connect(self.handle_connect)
        self.disconnect_btn.clicked.connect(self.handle_disconnect)

        self.disconnect_btn.setEnabled(False)

        btn_layout.addWidget(self.connect_btn)
        btn_layout.addWidget(self.disconnect_btn)
        form_layout.addRow(btn_layout)

        # --- Status Label ---
        self.status_label = QLabel("🟥 Status: Disconnected")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.status_label.setStyleSheet("color: #E53935;")
        form_layout.addRow(self.status_label)

        layout.addWidget(box, alignment=Qt.AlignCenter)
        self.setLayout(layout)

        # ✅ Load data from config if available
        self.load_previous_config()

    # ============================
    # STYLE HELPERS
    # ============================
    def _style_input(self, field: QLineEdit, font: QFont):
        field.setFont(font)
        field.setStyleSheet("""
            QLineEdit {
                border: 1.5px solid #90CAF9;
                border-radius: 10px;
                padding: 10px;
                background-color: #FAFAFA;
            }
            QLineEdit:focus {
                border: 2px solid #42A5F5;
                background-color: #FFFFFF;
            }
        """)

    def _style_button(self, button: QPushButton, color, hover, pressed):
        button.setFont(QFont("Segoe UI", 12, QFont.Bold))
        button.setCursor(Qt.PointingHandCursor)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border-radius: 10px;
                padding: 10px;
            }}
            QPushButton:hover {{
                background-color: {hover};
            }}
            QPushButton:pressed {{
                background-color: {pressed};
            }}
        """)

    # ============================
    # EVENT HANDLERS
    # ============================
    def handle_connect(self):
        """Emit connection signal"""
        server_ip = self.server_input.text().strip()
        port = self.port_input.text().strip()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not all([server_ip, port, username, password]):
            self.show_message("Error", "Please fill in all fields.", QMessageBox.Warning)
            return

        try:
            port = int(port)
        except ValueError:
            self.show_message("Error", "Port must be a number.", QMessageBox.Warning)
            return

        # ✅ Emit to main.py (to handle the actual connection)
        self.connection_requested.emit(server_ip, port, username, password)

    def handle_disconnect(self):
        """Emit disconnection signal"""
        if not self.connected:
            self.show_message("Info", "Already disconnected.", QMessageBox.Information)
            return

        self.disconnection_requested.emit()

    def update_connection_status(self, connected: bool, message: str = ""):
        """Update UI when connection state changes (called by main.py)"""
        self.connected = connected
        if connected:
            self.status_label.setText("🟩 Status: Connected")
            self.status_label.setStyleSheet("color: #43A047;")
            self.connect_btn.setEnabled(False)
            self.disconnect_btn.setEnabled(True)
        else:
            self.status_label.setText("🟥 Status: Disconnected")
            self.status_label.setStyleSheet("color: #E53935;")
            self.connect_btn.setEnabled(True)
            self.disconnect_btn.setEnabled(False)

        if message:
            self.show_message("Connection Status", message, QMessageBox.Information)

    def load_previous_config(self):
        """Load previously saved configuration"""
        if not self.config_data:
            return
        self.server_input.setText(self.config_data.get("server_ip", ""))
        self.port_input.setText(self.config_data.get("port", ""))
        self.username_input.setText(self.config_data.get("username", ""))
        self.password_input.setText(self.config_data.get("password", ""))

    def show_message(self, title, text, icon):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setIcon(icon)
        msg.exec_()
