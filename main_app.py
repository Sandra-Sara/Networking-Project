"""
PyQt5 File Transfer Client - Main Application Window (Used after Config/Login)
"""

import os
from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QVBoxLayout, QWidget,
    QMessageBox, QFileDialog
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QTimer

from client.file_server_client import FileServerClient
from auth.auth_service import AuthService
from threads.file_transfer_thread import FileTransferThread
from ui.styles import APP_STYLES
from ui.auth_tab import AuthTab
from ui.connection_tab import ConnectionTab
from ui.files_tab import FilesTab
from ui.logs_tab import LogsTab
from config import AppConfig


class FileTransferApp(QMainWindow):
    """Main application window with all tabs"""

    def __init__(self):
        super().__init__()
        self.client = FileServerClient()
        self.auth_service = AuthService()
        self.transfer_thread = None

        self.init_ui()
        self.connect_signals()

    # --------------------------------------------------------------------------
    # 🪟 UI INITIALIZATION
    # --------------------------------------------------------------------------
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle(f"{AppConfig.APP_NAME} - Your Digital Locker")
        self.setGeometry(100, 80, AppConfig.DEFAULT_WINDOW_WIDTH, AppConfig.DEFAULT_WINDOW_HEIGHT)
        self.setStyleSheet(APP_STYLES)
        self.set_window_icon()

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Create tab widget
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        # Create tabs
        self.auth_tab = AuthTab()
        self.connection_tab = ConnectionTab()
        self.files_tab = FilesTab()
        self.logs_tab = LogsTab()

        self.tabs.addTab(self.auth_tab, "Authentication")
        self.tabs.addTab(self.connection_tab, "Connection")
        self.tabs.addTab(self.files_tab, "Files")
        self.tabs.addTab(self.logs_tab, "Logs")

        # Disable Connection and Files tabs until login
        self.tabs.setTabEnabled(1, False)
        self.tabs.setTabEnabled(2, False)

    # --------------------------------------------------------------------------
    # ⚙️ SIGNAL CONNECTIONS
    # --------------------------------------------------------------------------
    def connect_signals(self):
        """Connect all signal handlers"""
        # Auth tab
        self.auth_tab.login_requested.connect(self.handle_login)
        self.auth_tab.logout_requested.connect(self.handle_logout)

        # Connection tab
        self.connection_tab.connection_requested.connect(self.handle_connection_request)
        self.connection_tab.disconnection_requested.connect(self.handle_disconnection_request)

        # Files tab
        self.files_tab.upload_requested.connect(self.handle_file_upload)
        self.files_tab.download_requested.connect(self.handle_file_download)
        self.files_tab.refresh_requested.connect(self.handle_files_refresh)
        self.files_tab.delete_requested.connect(self.handle_file_delete)

        # Logs tab
        self.logs_tab.export_logs_requested.connect(self.handle_export_logs)

    # --------------------------------------------------------------------------
    # 🔐 LOGIN & LOGOUT
    # --------------------------------------------------------------------------
    def handle_login(self, email: str, password: str):
        """Handle user login"""
        if not email or not password:
            QMessageBox.warning(self, "Login", "Please enter email and password")
            return

        success, message = self.auth_service.login(email, password)
        if success:
            self.auth_tab.update_auth_status(True, email)
            self.connection_tab.set_token_display(self.auth_service.get_token())
            self.tabs.setTabEnabled(1, True)
            self.tabs.setCurrentIndex(1)
            QMessageBox.information(self, "Login Successful", f"Welcome back!\n\nLogged in as: {email}")
        else:
            QMessageBox.critical(self, "Login Failed", message)

    def handle_logout(self):
        """Handle logout"""
        self.auth_service.logout()
        self.auth_tab.update_auth_status(False)
        self.connection_tab.clear_token_display()
        self.tabs.setTabEnabled(1, False)
        self.tabs.setTabEnabled(2, False)
        if self.client.socket:
            self.client.disconnect()
            self.connection_tab.update_connection_status(False)
        self.tabs.setCurrentIndex(0)
        QMessageBox.information(self, "Logout", "You have been logged out successfully")

    # --------------------------------------------------------------------------
    # 🔌 CONNECTION HANDLERS
    # --------------------------------------------------------------------------
    def handle_connection_request(self, host: str, port: int):
        """Handle connection request"""
        if not self.auth_service.is_authenticated():
            QMessageBox.warning(self, "Connection", "Please login first to get authentication token")
            return

        self.client.host = host
        self.client.port = port

        if self.client.connect():
            success, message = self.client.authenticate(self.auth_service.get_token())
            if success:
                self.connection_tab.update_connection_status(True, "Connected & Authenticated")
                self.tabs.setTabEnabled(2, True)
                self.tabs.setCurrentIndex(2)
                QMessageBox.information(self, "Success", "Connected and authenticated successfully")
            else:
                self.client.disconnect()
                self.connection_tab.update_connection_status(False, "Authentication failed")
                QMessageBox.critical(self, "Auth Error", f"Authentication failed:\n{message}")
        else:
            self.connection_tab.update_connection_status(False, "Connection failed")
            QMessageBox.critical(self, "Connection Error", "Failed to connect to server")

    def handle_disconnection_request(self):
        """Handle disconnection"""
        self.client.disconnect()
        self.connection_tab.update_connection_status(False, "Disconnected")
        self.tabs.setTabEnabled(2, False)
        self.tabs.setCurrentIndex(1)
        QMessageBox.information(self, "Disconnected", "Disconnected from server successfully")

    # --------------------------------------------------------------------------
    # 📁 FILE OPERATIONS
    # --------------------------------------------------------------------------
    def handle_file_upload(self, file_path: str):
        """Handle file upload"""
        if not self.client.socket or not self.client.authenticated:
            QMessageBox.warning(self, "Upload Error", "Please connect to server first")
            return

        filename = os.path.basename(file_path)
        self.transfer_thread = FileTransferThread(self.client, 'upload', file_path=file_path)
        self.transfer_thread.progress_updated.connect(self.files_tab.update_transfer_progress)
        self.transfer_thread.transfer_completed.connect(self.on_transfer_completed)
        self.transfer_thread.start()

    def handle_file_download(self, filename: str, save_path: str):
        """Handle file download"""
        if not self.client.socket or not self.client.authenticated:
            QMessageBox.warning(self, "Download Error", "Please connect to server first")
            return

        self.transfer_thread = FileTransferThread(
            self.client, 'download',
            filename=filename, save_path=save_path
        )
        self.transfer_thread.progress_updated.connect(self.files_tab.update_transfer_progress)
        self.transfer_thread.transfer_completed.connect(self.on_transfer_completed)
        self.transfer_thread.start()

    def on_transfer_completed(self, success: bool, message: str):
        """Handle transfer completion"""
        if success:
            self.files_tab.handle_transfer_success(message)
        else:
            self.files_tab.handle_transfer_error(message)

    def handle_files_refresh(self):
        """Refresh file list"""
        if not self.client.socket or not self.client.authenticated:
            QMessageBox.warning(self, "Refresh Error", "Please connect to server first")
            return

        success, files, message = self.client.list_files()
        if success:
            self.files_tab.update_files_list(files)
        else:
            QMessageBox.critical(self, "Error", message)

    def handle_file_delete(self, filename: str):
        """Handle file deletion"""
        if not self.client.socket or not self.client.authenticated:
            QMessageBox.warning(self, "Delete Error", "Please connect to server first")
            return

        success, message = self.client.delete_file(filename)
        if success:
            self.files_tab.handle_delete_success(message)
        else:
            self.files_tab.handle_delete_error(message)

    # --------------------------------------------------------------------------
    # 📜 LOG EXPORT & WINDOW ICON
    # --------------------------------------------------------------------------
    def handle_export_logs(self):
        """Export logs to a text file"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Logs", "file_transfer_logs.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.logs_tab.get_logs_text())
                QMessageBox.information(self, "Success", f"Logs exported to:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export logs:\n{e}")

    def set_window_icon(self):
        """Set the app window icon"""
        icon_paths = [
            "assets/icons/app_icon.png",
            "assets/app_icon.png",
            "icons/app_icon.png",
            "app_icon.png"
        ]
        for path in icon_paths:
            if os.path.exists(path):
                icon = QIcon(path)
                if not icon.isNull():
                    self.setWindowIcon(icon)
                    break
        else:
            self.create_fallback_icon()

    def create_fallback_icon(self):
        """Create fallback icon if no image exists"""
        from PyQt5.QtGui import QPixmap, QPainter
        from PyQt5.QtCore import Qt
        pixmap = QPixmap(32, 32)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        painter.setBrush(Qt.blue)
        painter.drawEllipse(0, 0, 32, 32)
        painter.setPen(Qt.white)
        painter.drawText(pixmap.rect(), Qt.AlignCenter, "DL")
        painter.end()
        self.setWindowIcon(QIcon(pixmap))
