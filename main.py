"""
Main controller for CryptPort App
Handles window transitions: Register → Login → Config → File Transfer
"""

import sys
from PyQt5.QtWidgets import QApplication
from ui.register_window import RegisterWindow
from ui.login_window import LoginWindow
from ui.config_window import ConfigWindow


class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.register_window = None
        self.login_window = None
        self.config_window = None

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
        """Show login window (only once)"""
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
        """Show server configuration window after login"""
        if self.login_window:
            self.login_window.close()

        if self.config_window:
            self.config_window.close()

        self.config_window = ConfigWindow()
        self.config_window.show()

    # ========================
    # 🚀 RUN APPLICATION
    # ========================
    def run(self):
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    controller = AppController()
    controller.run()
