"""
Main controller for CryptPort App
Handles window transitions: Register → Login → Config → Connection → File Transfer
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.register_window import RegisterWindow
from ui.login_window import LoginWindow
from ui.config_window import ConfigWindow
from ui.connection_tab import ConnectionTab  # ✅ newly added
from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget


class ConnectionWindow(QMainWindow):
    """Wrapper window for the ConnectionTab"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CryptPort - Connection")
        self.setGeometry(200, 100, 1000, 700)

        # Create central widget
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        # Add ConnectionTab
        self.connection_tab = ConnectionTab()
        layout.addWidget(self.connection_tab)

        self.setCentralWidget(central_widget)

        # Connect signals
        self.connection_tab.connection_requested.connect(self.on_connect_requested)
        self.connection_tab.disconnection_requested.connect(self.on_disconnect_requested)

    def on_connect_requested(self, host, port):
        """Handle connect button clicked"""
        # Simulate success
        print(f"Connecting to {host}:{port}")
        self.connection_tab.update_connection_status(True, "Connected successfully!")

    def on_disconnect_requested(self):
        """Handle disconnect"""
        print("Disconnected from server")
        self.connection_tab.update_connection_status(False, "Disconnected successfully")


class AppController:
    """Main controller managing window transitions"""

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.register_window = None
        self.login_window = None
        self.config_window = None
        self.connection_window = None  # ✅ new

        # Start with registration
        self.show_register_window()

    # ========================
    # 1️⃣ REGISTER WINDOW
    # ========================
    def show_register_window(self):
        """Show registration window"""
        if self.register_window:
            self.register_window.close()

        self.register_window = RegisterWindow()
        self.register_window.register_success.connect(self.show_login_window)
        self.register_window.show()

    # ========================
    # 2️⃣ LOGIN WINDOW
    # ========================
    def show_login_window(self):
        """Show login window"""
        if self.login_window:
            self.login_window.close()

        self.login_window = LoginWindow()
        self.login_window.login_success.connect(self.show_config_window)
        self.login_window.go_register.connect(self.show_register_window)
        self.login_window.show()

    # ========================
    # 3️⃣ CONFIG WINDOW
    # ========================
    def show_config_window(self, email=None):
        """Show server configuration window"""
        if self.login_window:
            self.login_window.close()
        if self.config_window:
            self.config_window.close()

        self.config_window = ConfigWindow()
        self.config_window.next_signal.connect(self.show_connection_window)  # ✅ add this signal in config_window
        self.config_window.show()

    # ========================
    # 4️⃣ CONNECTION WINDOW
    # ========================
    def show_connection_window(self):
        """Show the connection window after config"""
        if self.config_window:
            self.config_window.close()

        self.connection_window = ConnectionWindow()
        self.connection_window.show()

    # ========================
    # 🚀 RUN APPLICATION
    # ========================
    def run(self):
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    controller = AppController()
    controller.run()
