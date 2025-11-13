"""
Main controller for CryptPort App
Handles window transitions: Welcome → Register → Login → Config → Connection → File Transfer → Encryption / History
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from ui.welcome_window import WelcomeWindow
from ui.register_window import RegisterWindow
from ui.login_window import LoginWindow
from ui.config_window import ConfigWindow
from ui.connection_tab import ConnectionTab


class ConnectionWindow(QMainWindow):
    """Wrapper window for the ConnectionTab and other related tabs"""

    def __init__(self, controller, config_data=None):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("CryptPort - Connection")
        self.setGeometry(200, 100, 1000, 700)
        self.config_data = config_data or {}

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        self.connection_tab = ConnectionTab(self.config_data)
        layout.addWidget(self.connection_tab)
        self.setCentralWidget(central_widget)

        self.connection_tab.connection_requested.connect(self.on_connect_requested)
        self.connection_tab.disconnection_requested.connect(self.on_disconnect_requested)

        self.file_tab = None

    def on_connect_requested(self, host, port, username, password):
        print(f"Connecting to {host}:{port} with {username}/{password}")
        self.connection_tab.update_connection_status(True, "Connected successfully!")
        self.open_file_tab()

    def on_disconnect_requested(self):
        print("Disconnected from server")
        self.connection_tab.update_connection_status(False, "Disconnected successfully")

    def open_file_tab(self):
        from ui.file_tab import FileTab
        self.file_tab = FileTab()
        self.setCentralWidget(self.file_tab)

        self.file_tab.disconnect_requested.connect(self.return_to_config_window)
        self.file_tab.open_encryption_requested.connect(self.open_encryption_tab)
        self.file_tab.open_history_requested.connect(self.open_history_tab)

    def open_encryption_tab(self):
        from ui.encryption_tab import EncryptionTab
        self.encryption_tab = EncryptionTab()
        self.setCentralWidget(self.encryption_tab)
        self.encryption_tab.back_requested.connect(self.open_file_tab)

    def open_history_tab(self):
        from ui.history_tab import HistoryTab
        self.history_tab = HistoryTab()
        self.setCentralWidget(self.history_tab)
        self.history_tab.back_requested.connect(self.open_file_tab)

    def return_to_config_window(self):
        print("Returning to server configuration...")
        self.close()
        self.controller.show_config_window()


class AppController:
    """Main controller managing all window transitions"""

    def __init__(self):
        self.app = QApplication(sys.argv)
        self.welcome_window = None
        self.register_window = None
        self.login_window = None
        self.config_window = None
        self.connection_window = None
        self.config_data = {}

        # Start with Welcome Page
        self.show_welcome_window()

    # 0️⃣ WELCOME WINDOW
    def show_welcome_window(self):
        if self.welcome_window:
            self.welcome_window.close()
        self.welcome_window = WelcomeWindow()
        self.welcome_window.go_register.connect(self.show_register_window)
        self.welcome_window.go_login.connect(self.show_login_window)
        self.welcome_window.show()

    # 1️⃣ REGISTER WINDOW
    def show_register_window(self):
        if self.welcome_window:
            self.welcome_window.close()
        if self.register_window:
            self.register_window.close()
        self.register_window = RegisterWindow()
        self.register_window.register_success.connect(self.show_login_window)
        self.register_window.show()

    # 2️⃣ LOGIN WINDOW
    def show_login_window(self):
        if self.welcome_window:
            self.welcome_window.close()
        if self.login_window:
            self.login_window.close()
        self.login_window = LoginWindow()
        self.login_window.login_success.connect(self.show_config_window)
        self.login_window.go_register.connect(self.show_register_window)
        self.login_window.show()

    # 3️⃣ CONFIG WINDOW
    def show_config_window(self, email=None):
        if self.login_window:
            self.login_window.close()
        if self.connection_window:
            self.connection_window.close()
        if self.config_window:
            self.config_window.close()

        self.config_window = ConfigWindow()
        self.config_window.config_complete.connect(self.show_connection_window)
        self.config_window.show()

    # 4️⃣ CONNECTION WINDOW
    def show_connection_window(self, config_data=None):
        if self.config_window:
            self.config_window.close()
        if config_data:
            self.config_data = config_data
        self.connection_window = ConnectionWindow(self, self.config_data)
        self.connection_window.show()

    def run(self):
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    controller = AppController()
    controller.run()
