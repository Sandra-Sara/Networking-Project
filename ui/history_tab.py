"""
HistoryTab for CryptPort
Displays a log of file transfer and encryption activities.
Styled consistently with other CryptPort pages.
"""

import os
import datetime
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton,
    QListWidget, QHBoxLayout, QFrame, QMessageBox
)
from PyQt5.QtGui import QFont, QColor, QPalette
from PyQt5.QtCore import Qt, pyqtSignal


class HistoryTab(QWidget):
    """Activity history page"""
    back_requested = pyqtSignal()  # ✅ Signal to go back to FileTab

    def __init__(self):
        super().__init__()
        self.history_file = os.path.join(os.getcwd(), "cryptport_history.log")
        self.init_ui()
        self.load_history()

    def init_ui(self):
        # Background
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor("#E3F2FD"))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(25)

        # Title
        title = QLabel("📜 File Activity History")
        title.setFont(QFont("Segoe UI", 22, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("View records of sent, received, encrypted, and decrypted files.")
        subtitle.setFont(QFont("Segoe UI", 12))
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("color: gray;")

        layout.addWidget(title)
        layout.addWidget(subtitle)

        # White Box
        box = QFrame()
        box.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                border: 2px solid #BBDEFB;
            }
        """)
        box_layout = QVBoxLayout(box)
        box_layout.setContentsMargins(25, 25, 25, 25)
        box_layout.setSpacing(15)

        # History List
        self.history_list = QListWidget()
        self.history_list.setStyleSheet("""
            QListWidget {
                border: 1.5px solid #BBDEFB;
                border-radius: 10px;
                padding: 8px;
                background-color: #FAFAFA;
                font-size: 13px;
            }
        """)
        box_layout.addWidget(self.history_list)

        # Buttons Row
        button_row = QHBoxLayout()
        button_row.setAlignment(Qt.AlignCenter)
        button_row.setSpacing(20)

        # 🔄 Refresh Button
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.refresh_btn.setCursor(Qt.PointingHandCursor)
        self.refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #64B5F6;
                color: white;
                border-radius: 8px;
                padding: 8px 20px;
            }
            QPushButton:hover { background-color: #1E88E5; }
        """)
        self.refresh_btn.clicked.connect(self.load_history)

        # 🗑️ Clear Button
        self.clear_btn = QPushButton("🗑️ Clear History")
        self.clear_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.clear_btn.setCursor(Qt.PointingHandCursor)
        self.clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #E57373;
                color: white;
                border-radius: 8px;
                padding: 8px 20px;
            }
            QPushButton:hover { background-color: #D32F2F; }
        """)
        self.clear_btn.clicked.connect(self.clear_history)

        # ⬅️ Back Button
        self.back_btn = QPushButton("⬅ Back to File Transfer")
        self.back_btn.setFont(QFont("Segoe UI", 12, QFont.Bold))
        self.back_btn.setCursor(Qt.PointingHandCursor)
        self.back_btn.setStyleSheet("""
            QPushButton {
                background-color: #81C784;
                color: white;
                border-radius: 8px;
                padding: 8px 25px;
            }
            QPushButton:hover { background-color: #388E3C; }
        """)
        self.back_btn.clicked.connect(self.on_back_clicked)

        button_row.addWidget(self.refresh_btn)
        button_row.addWidget(self.clear_btn)
        button_row.addWidget(self.back_btn)

        box_layout.addLayout(button_row)
        layout.addWidget(box, alignment=Qt.AlignCenter)

    # ========================
    #  Functionality
    # ========================

    def load_history(self):
        """Load previous file activities"""
        self.history_list.clear()

        if not os.path.exists(self.history_file):
            with open(self.history_file, "w") as f:
                f.write("=== CryptPort File History ===\n")
            self.history_list.addItem("No activity recorded yet.")
            return

        with open(self.history_file, "r") as f:
            lines = f.readlines()

        if len(lines) <= 1:
            self.history_list.addItem("No activity recorded yet.")
        else:
            for line in lines[1:]:
                self.history_list.addItem(line.strip())

    def add_entry(self, action: str, filename: str):
        """Add a new entry to history"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] {action}: {filename}"

        with open(self.history_file, "a") as f:
            f.write(entry + "\n")

        self.history_list.addItem(entry)

    def clear_history(self):
        """Clear all saved history"""
        confirm = QMessageBox.question(
            self, "Clear History", "Are you sure you want to clear all records?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            open(self.history_file, "w").write("=== CryptPort File History ===\n")
            self.history_list.clear()
            self.history_list.addItem("History cleared.")

    def on_back_clicked(self):
        """Go back to the FileTab"""
        self.back_requested.emit()
