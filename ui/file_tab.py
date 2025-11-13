"""
File Transfer Window for CryptPort
Styled consistently with Register and Config pages
Now includes 'Encryption' and 'History' buttons for navigation.
"""

import os
import sys
import subprocess
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog,
    QProgressBar, QListWidget, QHBoxLayout, QFrame, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor, QPalette


class FileTab(QWidget):
    """File Transfer Page"""
    disconnect_requested = pyqtSignal()   # 🔙 Go back to connection page
    open_encryption_requested = pyqtSignal()  # ➡️ Go to encryption page
    open_history_requested = pyqtSignal()     # ➡️ Go to history page

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Window setup
        self.setWindowTitle("CryptPort - File Transfer")
        self.setFixedSize(1000, 700)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#E3F2FD"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        # --- Main layout ---
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)
        main_layout.setSpacing(30)

        # --- Title Section ---
        title = QLabel("📂 Secure File Transfer")
        title.setFont(QFont("Segoe UI", 26, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Send and receive encrypted files safely 🔒")
        subtitle.setFont(QFont("Segoe UI", 13))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: gray; font-weight: 500;")

        main_layout.addWidget(title)
        main_layout.addWidget(subtitle)

        # --- Central White Box ---
        box = QFrame()
        box.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 18px;
                border: 2px solid #BBDEFB;
            }
        """)
        box.setFixedWidth(700)
        box_layout = QVBoxLayout(box)
        box_layout.setContentsMargins(60, 50, 60, 50)
        box_layout.setSpacing(25)

        # --- SEND FILE SECTION ---
        send_title = QLabel("📤 Send File")
        send_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        box_layout.addWidget(send_title)

        send_row = QHBoxLayout()
        self.choose_btn = QPushButton("Choose File...")
        self.choose_btn.setFont(QFont("Segoe UI", 12))
        self.choose_btn.setCursor(Qt.PointingHandCursor)
        self.choose_btn.setStyleSheet("""
            QPushButton {
                background-color: #E3F2FD;
                color: #1565C0;
                border-radius: 10px;
                padding: 10px 16px;
            }
            QPushButton:hover { background-color: #BBDEFB; }
        """)
        self.choose_btn.clicked.connect(self.choose_file)

        self.send_btn = QPushButton("Send Securely 🚀")
        self.send_btn.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.send_btn.setCursor(Qt.PointingHandCursor)
        self.send_btn.setStyleSheet("""
            QPushButton {
                background-color: #42A5F5;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
            }
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.send_btn.clicked.connect(self.send_file)

        send_row.addWidget(self.choose_btn)
        send_row.addWidget(self.send_btn)
        box_layout.addLayout(send_row)

        # --- Progress Bar ---
        self.progress = QProgressBar()
        self.progress.setValue(0)
        self.progress.setFixedHeight(25)
        self.progress.setStyleSheet("""
            QProgressBar {
                border: 1.5px solid #90CAF9;
                border-radius: 10px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #42A5F5;
                border-radius: 8px;
            }
        """)
        box_layout.addWidget(self.progress)

        # --- RECEIVED FILES SECTION ---
        recv_title = QLabel("📥 Received Files")
        recv_title.setFont(QFont("Segoe UI", 16, QFont.Bold))
        box_layout.addWidget(recv_title)

        self.file_list = QListWidget()
        self.file_list.setStyleSheet("""
            QListWidget {
                border: 1.5px solid #BBDEFB;
                border-radius: 10px;
                padding: 8px;
                background-color: #FAFAFA;
            }
        """)
        box_layout.addWidget(self.file_list)

        self.open_folder_btn = QPushButton("📁 Open Folder")
        self.open_folder_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.open_folder_btn.setCursor(Qt.PointingHandCursor)
        self.open_folder_btn.setStyleSheet("""
            QPushButton {
                background-color: #64B5F6;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
            }
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.open_folder_btn.clicked.connect(self.open_folder)
        box_layout.addWidget(self.open_folder_btn, alignment=Qt.AlignCenter)

        main_layout.addWidget(box, alignment=Qt.AlignCenter)

        # --- Bottom Buttons ---
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(30)
        bottom_row.setAlignment(Qt.AlignCenter)

        # Disconnect
        self.disconnect_btn = QPushButton("🔙 Disconnect")
        self.disconnect_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.disconnect_btn.setCursor(Qt.PointingHandCursor)
        self.disconnect_btn.setStyleSheet("""
            QPushButton {
                background-color: #E57373;
                color: white;
                border-radius: 10px;
                padding: 10px 25px;
            }
            QPushButton:hover { background-color: #D32F2F; }
        """)
        self.disconnect_btn.clicked.connect(self.disconnect_requested.emit)

        # Encryption Button
        self.encryption_btn = QPushButton("🛡️ Encryption / Decryption")
        self.encryption_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.encryption_btn.setCursor(Qt.PointingHandCursor)
        self.encryption_btn.setStyleSheet("""
            QPushButton {
                background-color: #81C784;
                color: white;
                border-radius: 10px;
                padding: 10px 25px;
            }
            QPushButton:hover { background-color: #66BB6A; }
        """)
        self.encryption_btn.clicked.connect(self.open_encryption_requested.emit)

        # History Button
        self.history_btn = QPushButton("📜 History")
        self.history_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.history_btn.setCursor(Qt.PointingHandCursor)
        self.history_btn.setStyleSheet("""
            QPushButton {
                background-color: #FFD54F;
                color: black;
                border-radius: 10px;
                padding: 10px 25px;
            }
            QPushButton:hover { background-color: #FFCA28; }
        """)
        self.history_btn.clicked.connect(self.open_history_requested.emit)

        bottom_row.addWidget(self.disconnect_btn)
        bottom_row.addWidget(self.encryption_btn)
        bottom_row.addWidget(self.history_btn)

        main_layout.addLayout(bottom_row)
        self.setLayout(main_layout)

        # State
        self.selected_file = None
        self.timer = QTimer()
        self.timer.timeout.connect(self.simulate_progress)

        # Folder path
        self.transfer_folder = os.path.join(os.getcwd(), "cryptport_transfers")
        if not os.path.exists(self.transfer_folder):
            os.makedirs(self.transfer_folder)

    # ======================
    # Functionality
    # ======================

    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Send")
        if file_path:
            self.selected_file = file_path
            QMessageBox.information(self, "File Selected", f"Selected file:\n{file_path}")

    def send_file(self):
        if not self.selected_file:
            QMessageBox.warning(self, "No File", "Please choose a file first.")
            return

        QMessageBox.information(self, "Encrypting", "Encrypting file before sending...")
        self.progress.setValue(0)
        self.timer.start(100)  # simulate sending

    def simulate_progress(self):
        val = self.progress.value() + 5
        if val <= 100:
            self.progress.setValue(val)
        else:
            self.timer.stop()
            # Simulate "saving" sent file to local folder
            filename = os.path.basename(self.selected_file)
            target_path = os.path.join(self.transfer_folder, filename)
            with open(self.selected_file, "rb") as src, open(target_path, "wb") as dst:
                dst.write(src.read())

            self.file_list.addItem(f"Sent: {filename}")
            self.selected_file = None
            self.progress.setValue(0)
            QMessageBox.information(self, "Success", f"File sent and saved to:\n{target_path}")

    def open_folder(self):
        """Open the transfer folder in file explorer"""
        if not os.path.exists(self.transfer_folder):
            os.makedirs(self.transfer_folder)

        path = os.path.realpath(self.transfer_folder)

        # Open according to OS
        if sys.platform.startswith('win'):
            os.startfile(path)
        elif sys.platform.startswith('darwin'):
            subprocess.Popen(['open', path])
        else:
            subprocess.Popen(['xdg-open', path])
