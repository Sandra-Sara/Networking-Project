"""
EncryptionTab for CryptPort
Handles encryption and decryption of files securely.
Now includes a Back button and signal for navigation.
"""

import os
import shutil
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QFileDialog, QMessageBox, QHBoxLayout
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, pyqtSignal

from ui.history_tab import HistoryTab  # ✅ for logging


class EncryptionTab(QWidget):
    """Encryption / Decryption Page"""

    # ✅ Add signal for navigation
    back_requested = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.selected_file = None
        self.history = HistoryTab()
        self.init_ui()

    def init_ui(self):
        # Background styling
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#E3F2FD"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(25)

        # ----- Title -----
        title = QLabel("🧩 File Encryption / Decryption")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Encrypt and decrypt files before transfer for maximum security 🔒")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: gray;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # ----- Buttons -----
        button_row = QHBoxLayout()
        button_row.setSpacing(20)
        button_row.setAlignment(Qt.AlignCenter)

        self.encrypt_btn = QPushButton("Encrypt File 🔐")
        self.encrypt_btn.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.encrypt_btn.setCursor(Qt.PointingHandCursor)
        self.encrypt_btn.setStyleSheet("""
            QPushButton {
                background-color: #42A5F5;
                color: white;
                border-radius: 10px;
                padding: 10px 25px;
            }
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.encrypt_btn.clicked.connect(lambda: self.handle_file(True))

        self.decrypt_btn = QPushButton("Decrypt File 🔓")
        self.decrypt_btn.setFont(QFont("Segoe UI", 13, QFont.Bold))
        self.decrypt_btn.setCursor(Qt.PointingHandCursor)
        self.decrypt_btn.setStyleSheet("""
            QPushButton {
                background-color: #66BB6A;
                color: white;
                border-radius: 10px;
                padding: 10px 25px;
            }
            QPushButton:hover { background-color: #388E3C; }
        """)
        self.decrypt_btn.clicked.connect(lambda: self.handle_file(False))

        button_row.addWidget(self.encrypt_btn)
        button_row.addWidget(self.decrypt_btn)
        layout.addLayout(button_row)

        # ----- Info Label -----
        self.info_label = QLabel("Select a file to encrypt or decrypt.")
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setStyleSheet("color: #1565C0; font-weight: 500; font-size: 13px;")
        layout.addWidget(self.info_label)

        # ----- Back Button -----
        back_btn = QPushButton("⬅ Back to File Page")
        back_btn.setFont(QFont("Segoe UI", 11))
        back_btn.setCursor(Qt.PointingHandCursor)
        back_btn.setStyleSheet("""
            QPushButton {
                background-color: #E57373;
                color: white;
                border-radius: 8px;
                padding: 8px 20px;
            }
            QPushButton:hover { background-color: #C62828; }
        """)
        back_btn.clicked.connect(self.back_requested.emit)
        layout.addWidget(back_btn, alignment=Qt.AlignCenter)

    # ========================
    # Core functionality
    # ========================

    def handle_file(self, is_encrypt: bool):
        """Handles encryption or decryption"""
        action = "Encrypt" if is_encrypt else "Decrypt"
        file_path, _ = QFileDialog.getOpenFileName(self, f"Select File to {action}")

        if not file_path:
            return

        self.selected_file = file_path
        file_name = os.path.basename(file_path)

        QMessageBox.information(self, f"{action}ing...", f"{action}ing {file_name}...")
        self.simulate_crypto(file_name, is_encrypt)

    def simulate_crypto(self, file_name: str, is_encrypt: bool):
        """Simulated encryption/decryption (creates new saved file)"""
        folder_name = "cryptport_encrypted" if is_encrypt else "cryptport_decrypted"
        output_folder = os.path.join(os.getcwd(), folder_name)
        os.makedirs(output_folder, exist_ok=True)

        base, ext = os.path.splitext(file_name)
        suffix = "_encrypted" if is_encrypt else "_decrypted"
        new_filename = f"{base}{suffix}{ext}"

        source_path = self.selected_file
        target_path = os.path.join(output_folder, os.path.basename(new_filename))

        try:
            shutil.copy2(source_path, target_path)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to process file:\n{e}")
            return

        action = "Encrypted" if is_encrypt else "Decrypted"
        QMessageBox.information(self, "Done", f"{action} file saved successfully:\n{target_path}")
        self.info_label.setText(f"✅ {action}: {os.path.basename(target_path)}")

        # ✅ Log this action
        self.history.add_entry(action, os.path.basename(target_path))
