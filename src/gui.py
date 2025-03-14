"""
File: gui.py
Author: Alex Mees
Date: 2025-03-13
Description: Scripts visualization
License: MIT
"""
# Standard library imports
import sys

# Third-party imports
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QPushButton, QWidget

# Local application imports


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

        # === Vertical Stack of Buttons ===
        button_layout = QVBoxLayout()  # Vertical stack
        buttons = ["Add", "Edit", "Delete", "Refresh"]
        for name in buttons:
            button = QPushButton(name)
            button_layout.addWidget(button)
        
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
        main_layout.addWidget(self.table)          # Spreadsheet (right)

        central_widget.setLayout(main_layout)

        # === Apply StyleSheet ===
        self.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QTableWidget {
                border: 2px solid #ccc;
                gridline-color: #aaa;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #2c3e50;
                color: white;
                padding: 4px;
            }
        """)
    
    def set_headers(self,headers):
        self.table.setHorizontalHeaderLabels(headers)

    def set_data_table(self,data):
        for row, rowData in enumerate(data):
            for col, value in enumerate(rowData):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
