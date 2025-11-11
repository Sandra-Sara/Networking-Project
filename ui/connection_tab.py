"""
Connection tab UI components with modern design
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QFormLayout, QGroupBox, 
                           QLineEdit, QPushButton, QLabel, QHBoxLayout, QFrame,
                           QStackedWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from .loading_spinner import LoadingSpinner
from config import AppConfig 

class ConnectionTab(QWidget):
    """Connection tab widget with modern design"""
    
    connection_requested = pyqtSignal(str, int)
    disconnection_requested = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.is_connected = False
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the connection UI with modern design"""
        layout = QVBoxLayout(self)
        layout.setSpacing(30)
        
        # Create stacked widget for different states
        self.stacked_widget = QStackedWidget()
        layout.addWidget(self.stacked_widget)
        
        # Create pages
        self.disconnected_page = self.create_disconnected_page()
        self.connected_page = self.create_connected_page()
        
        # Add pages to stack
        self.stacked_widget.addWidget(self.disconnected_page)
        self.stacked_widget.addWidget(self.connected_page)
        
        # Start with disconnected page
        self.stacked_widget.setCurrentWidget(self.disconnected_page)
    
    def create_disconnected_page(self):
        """Create the disconnected state page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(30)
        
        # Header section
        header_frame = QFrame()
        header_frame.setFrameStyle(QFrame.Box)
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setAlignment(Qt.AlignCenter)
        header_layout.setSpacing(15)
        
        # Title
        title_label = QLabel("Socket Server Connection")
        title_font = QFont()
        title_font.setPointSize(20)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #2c3e50; margin: 10px;")
        header_layout.addWidget(title_label)
        
        # Status
        self.disconnected_status_label = QLabel("Ready to connect")
        status_font = QFont()
        status_font.setPointSize(12)
        self.disconnected_status_label.setFont(status_font)
        self.disconnected_status_label.setAlignment(Qt.AlignCenter)
        self.disconnected_status_label.setStyleSheet("color: #7f8c8d; margin: 5px;")
        header_layout.addWidget(self.disconnected_status_label)
        
        layout.addWidget(header_frame)
        
        # Connection form
        conn_group = QGroupBox("Server Configuration")
        conn_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px;
                padding-top: 15px;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
                color: #2c3e50;
            }
        """)
        conn_layout = QFormLayout(conn_group)
        conn_layout.setSpacing(20)
        
        # Host input - use centralized config for default
        default_host, default_port = AppConfig.get_socket_config()
        self.host_input = QLineEdit(default_host)
        self.host_input.setPlaceholderText("Enter server hostname or IP address")
        self.host_input.setMinimumHeight(40)
        self.host_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        conn_layout.addRow("Host:", self.host_input)
        
        # Port input - use centralized config for default
        self.port_input = QLineEdit(str(default_port))
        self.port_input.setPlaceholderText("Enter port number")
        self.port_input.setMinimumHeight(40)
        self.port_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        conn_layout.addRow("Port:", self.port_input)
        
        # Connect button with loading state
        connect_button_layout = QHBoxLayout()
        self.connect_btn = QPushButton("Connect to Server")
        self.connect_btn.setMinimumHeight(50)
        self.connect_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                padding: 15px 30px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        self.connect_btn.clicked.connect(self.on_connect_clicked)
        
        self.connect_spinner = LoadingSpinner()
        self.connect_spinner.hide()
        
        connect_button_layout.addWidget(self.connect_btn)
        connect_button_layout.addWidget(self.connect_spinner)
        connect_button_layout.addStretch()
        
        conn_layout.addRow(connect_button_layout)
        
        layout.addWidget(conn_group)
        
        # Token info section
        token_group = QGroupBox("Authentication Status")
        token_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px;
                padding-top: 15px;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
                color: #2c3e50;
            }
        """)
        token_layout = QFormLayout(token_group)
        token_layout.setSpacing(15)
        
        self.token_display = QLineEdit()
        self.token_display.setReadOnly(True)
        self.token_display.setPlaceholderText("Login first to get authentication token")
        self.token_display.setMinimumHeight(40)
        self.token_display.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e9ecef;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: #f8f9fa;
                color: #7f8c8d;
            }
        """)
        token_layout.addRow("Token:", self.token_display)
        
        layout.addWidget(token_group)
        layout.addStretch()
        
        return page
    
    def create_connected_page(self):
        """Create the connected state page"""
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(30)
        
        # Success status section
        status_frame = QFrame()
        status_frame.setFrameStyle(QFrame.Box)
        status_frame.setStyleSheet("""
            QFrame {
                background-color: #d5f4e6;
                border: 2px solid #27ae60;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        status_layout = QVBoxLayout(status_frame)
        status_layout.setAlignment(Qt.AlignCenter)
        status_layout.setSpacing(15)
        
        # Success icon/text
        success_label = QLabel("✓ Connected to Server")
        success_font = QFont()
        success_font.setPointSize(20)
        success_font.setBold(True)
        success_label.setFont(success_font)
        success_label.setAlignment(Qt.AlignCenter)
        success_label.setStyleSheet("color: #27ae60; margin: 10px;")
        status_layout.addWidget(success_label)
        
        # Connection details
        self.connection_details_label = QLabel("Connected to localhost:8889")
        details_font = QFont()
        details_font.setPointSize(14)
        self.connection_details_label.setFont(details_font)
        self.connection_details_label.setAlignment(Qt.AlignCenter)
        self.connection_details_label.setStyleSheet("color: #2c3e50; margin: 5px;")
        status_layout.addWidget(self.connection_details_label)
        
        # Status message
        status_message = QLabel("File transfer operations are now available")
        status_message.setAlignment(Qt.AlignCenter)
        status_message.setStyleSheet("color: #7f8c8d; margin: 5px;")
        status_layout.addWidget(status_message)
        
        layout.addWidget(status_frame)
        
        # Connection info section
        info_group = QGroupBox("Connection Information")
        info_group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                margin-top: 10px;
                padding-top: 15px;
                border: 2px solid #e9ecef;
                border-radius: 8px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
                color: #2c3e50;
            }
        """)
        info_layout = QFormLayout(info_group)
        info_layout.setSpacing(15)
        
        # Server details (read-only)
        self.connected_host_display = QLineEdit()
        self.connected_host_display.setReadOnly(True)
        self.connected_host_display.setMinimumHeight(35)
        self.connected_host_display.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e9ecef;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: #f8f9fa;
                color: #2c3e50;
            }
        """)
        info_layout.addRow("Server Host:", self.connected_host_display)
        
        self.connected_port_display = QLineEdit()
        self.connected_port_display.setReadOnly(True)
        self.connected_port_display.setMinimumHeight(35)
        self.connected_port_display.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e9ecef;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: #f8f9fa;
                color: #2c3e50;
            }
        """)
        info_layout.addRow("Server Port:", self.connected_port_display)
        
        # Current token display
        self.connected_token_display = QLineEdit()
        self.connected_token_display.setReadOnly(True)
        self.connected_token_display.setMinimumHeight(35)
        self.connected_token_display.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e9ecef;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: #f8f9fa;
                color: #7f8c8d;
            }
        """)
        info_layout.addRow("Auth Token:", self.connected_token_display)
        
        layout.addWidget(info_group)
        
        # Disconnect button
        disconnect_layout = QHBoxLayout()
        self.disconnect_btn = QPushButton("Disconnect from Server")
        self.disconnect_btn.setMinimumHeight(50)
        self.disconnect_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
                padding: 15px 30px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        self.disconnect_btn.clicked.connect(self.disconnection_requested.emit)
        
        disconnect_layout.addWidget(self.disconnect_btn)
        disconnect_layout.addStretch()
        
        layout.addLayout(disconnect_layout)
        layout.addStretch()
        
        return page
    
    def on_connect_clicked(self):
        """Handle connect button click"""
        try:
            host = self.host_input.text().strip()
            port = int(self.port_input.text().strip())
            
            # Set loading state
            self.set_connecting_state(True)
            
            # Emit connection request
            self.connection_requested.emit(host, port)
        except ValueError:
            self.set_connecting_state(False)
            self.disconnected_status_label.setText("Invalid port number")
            self.disconnected_status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
    
    def set_connecting_state(self, connecting=True):
        """Set connecting loading state"""
        if connecting:
            self.connect_btn.setText("Connecting...")
            self.connect_btn.setEnabled(False)
            self.connect_spinner.show()
            self.connect_spinner.start()
            self.host_input.setEnabled(False)
            self.port_input.setEnabled(False)
            self.disconnected_status_label.setText("Establishing connection...")
            self.disconnected_status_label.setStyleSheet("color: #f39c12; font-weight: bold;")
        else:
            self.connect_btn.setText("Connect to Server")
            self.connect_btn.setEnabled(True)
            self.connect_spinner.stop()
            self.connect_spinner.hide()
            self.host_input.setEnabled(True)
            self.port_input.setEnabled(True)
            if not self.is_connected:
                self.disconnected_status_label.setText("Ready to connect")
                self.disconnected_status_label.setStyleSheet("color: #7f8c8d; font-weight: normal;")
    
    def get_connection_details(self) -> tuple[str, int]:
        """Get host and port from inputs"""
        return self.host_input.text().strip(), int(self.port_input.text().strip())
    
    def set_token_display(self, token: str):
        """Set the token display"""
        display_token = token[:50] + "..." if len(token) > 50 else token
        self.token_display.setText(display_token)
        self.connected_token_display.setText(display_token)
    
    def clear_token_display(self):
        """Clear the token display"""
        self.token_display.clear()
        self.connected_token_display.clear()
    
    def update_connection_status(self, connected: bool, message: str = ""):
        """Update connection status and switch pages"""
        self.is_connected = connected
        self.set_connecting_state(False)  # Reset loading state
        
        if connected:
            # Update connected page info
            host, port = self.get_connection_details()
            self.connection_details_label.setText(f"Connected to {host}:{port}")
            self.connected_host_display.setText(host)
            self.connected_port_display.setText(str(port))
            
            # Switch to connected page
            self.stacked_widget.setCurrentWidget(self.connected_page)
        else:
            # Update disconnected page status
            if message:
                if "error" in message.lower() or "failed" in message.lower():
                    self.disconnected_status_label.setText(message)
                    self.disconnected_status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
                else:
                    self.disconnected_status_label.setText(message)
                    self.disconnected_status_label.setStyleSheet("color: #7f8c8d; font-weight: normal;")
            else:
                self.disconnected_status_label.setText("Not connected")
                self.disconnected_status_label.setStyleSheet("color: #7f8c8d; font-weight: normal;")
            
            # Switch to disconnected page
            self.stacked_widget.setCurrentWidget(self.disconnected_page)
    
    def handle_connection_error(self, error_message: str):
        """Handle connection error"""
        self.set_connecting_state(False)
        self.disconnected_status_label.setText(f"Connection failed: {error_message}")
        self.disconnected_status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")