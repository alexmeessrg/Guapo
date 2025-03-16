"""
File: gui.py
Author: Alex Mees
Date: 2025-03-13
Description: Scripts visualization
License: MIT
"""
# Standard library imports
import sys
import os

# Third-party imports
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QMenuBar
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt, QSize

# Local application imports
from . import styles


class MainWindow(QMainWindow):
    def __init__(self):
    
        super().__init__()

        self.setWindowTitle("Guapo Data Handler")
        self.setGeometry(100, 100, 600, 400)
        self.showMaximized()

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout()  # Horizontal stack

        # Menu Bar
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu("File")
        data_menu = menubar.addMenu("Data")
        analysis_menu = menubar.addMenu("Analysis")
        settings_menu = menubar.addMenu("Settings")

        # Create actions
        open_action = QAction("Open", self)
        save_action = QAction("Save", self)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)  # Connect Exit action

        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()  # Adds a separator line
        file_menu.addAction(exit_action)

        # === Vertical Stack of Buttons ===
        button_layout = QVBoxLayout()  # Vertical stack
        button_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        buttons = ["Add", "Edit", "Delete", "Refresh"]
        buttons_icons = ["../assets/icons/icon_data.png", "../assets/icons/icon_clean.png","../assets/icons/icon_data.png","../assets/icons/icon_data.png"]
        for index, name in enumerate(buttons):
            button = QPushButton()
            button.setToolTip(name)
            button.setIcon(QIcon(os.path.join(os.path.dirname(__file__), buttons_icons[index])))
            button.setIconSize(QSize(48,48))
            button.setFixedSize(52,52)
            button_layout.addWidget(button)
        
        # === Set of tools (to the left) === 
        tools_layout = QVBoxLayout()
        tools_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        for name in buttons:
            button = QPushButton()
            button.setToolTip(name)
            button.setIcon(QIcon(os.path.join(os.path.dirname(__file__), "../assets/icons/icon_data.png")))
            button.setIconSize(QSize(48,48))
            button.setFixedSize(192,52)
            tools_layout.addWidget(button)


        # === Spreadsheet (QTableWidget) ===
        self.table = QTableWidget(20, 4)  # 5 rows, 3 columns
        
        
        # Fill the table with sample data
        data = [
            ["Alice", "25", "New York"],
            ["Bob", "30", "London"],
            ["Charlie", "22", "Berlin"],
            ["Diana", "28", "Tokyo"],
            ["Eve", "35", "Paris"],
        ]
        for row, rowData in enumerate(data):
            for col, value in enumerate(rowData):
                self.table.setItem(row, col, QTableWidgetItem(value))
        
        # === Add Widgets to Main Layout ===
        main_layout.addLayout(button_layout)  # Vertical button stack (left)
        main_layout.addLayout(tools_layout)
        main_layout.addWidget(self.table)          # Spreadsheet (right)

        central_widget.setLayout(main_layout)

        # === Apply StyleSheet ===
        self.setStyleSheet(styles.GUIStyles.style_sheet)
    
    def set_headers(self,headers):
        self.table.setHorizontalHeaderLabels(headers)

    def set_data_table(self,data):
        for row, rowData in enumerate(data):
            for col, value in enumerate(rowData):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
