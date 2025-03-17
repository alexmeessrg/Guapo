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

def _CreateButton(name='',fixedsize=[52,52],iconpath=None,iconsize=[48,48],tooltip=None) -> QPushButton:
        button = QPushButton(name)
        
        if (tooltip):
            button.setToolTip(tooltip)

        if (iconpath):
            button.setIcon(QIcon(os.path.join(os.path.dirname(__file__), iconpath)))
            button.setIconSize(QSize(iconsize[0],iconsize[1]))
        
        button.setFixedSize(fixedsize[0], fixedsize[1])
        return button


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
        
        # === Set of string tools  === 
        tools_layout = QVBoxLayout()
        tools_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        
        # Button for String Operations
        self.b_str_blocked = _CreateButton('Blocked List',[192,52],"../assets/icons/icon_data.png",[48,48],'Replaces selected words with ****.')
        self.b_str_dictionary = _CreateButton('Dictionary',[192,52],"../assets/icons/icon_data.png",[48,48],'Replaces a list of words by another.')
        self.b_str_statistics = _CreateButton('String Statistics',[192,52],"../assets/icons/icon_data.png",[48,48],'Basic statistics for string data.')
        self.b_str_capitalize = _CreateButton('Capitalize',[192,52],"../assets/icons/icon_data.png",[48,48],'Sets capitalization rule.')
        self.b_str_duplicates = _CreateButton('Duplicates',[192,52],"../assets/icons/icon_data.png",[48,48],'Identify duplicate data.')
        self.b_str_whitespaces = _CreateButton('White Spaces',[192,52],"../assets/icons/icon_data.png",[48,48],'Handles whitespace cleaning.')
        self.b_str_breakcolumn = _CreateButton('Split on Delimiter',[192,52],"../assets/icons/icon_data.png",[48,48],'Split a data column in 2 or more, acoording to specified delimiter.')


        tools_layout.addWidget(self.b_str_blocked)
        tools_layout.addWidget(self.b_str_dictionary)
        tools_layout.addWidget(self.b_str_statistics)
        tools_layout.addWidget(self.b_str_capitalize)
        tools_layout.addWidget(self.b_str_duplicates)
        tools_layout.addWidget(self.b_str_whitespaces)
        tools_layout.addWidget(self.b_str_breakcolumn)






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

    def set_event_handlers(self, target_button, function): #use this to add main.py functions to the GUI buttons.
        match target_button:
            case "b_str_blocked":
                self.b_str_blocked.clicked.connect(function)
            case "b_str_whitespace":
                self.b_str_whitespaces.clicked(function)
    
    def set_headers(self,headers):
        self.table.setHorizontalHeaderLabels(headers)

    def set_data_table(self,data):
        for row, rowData in enumerate(data):
            for col, value in enumerate(rowData):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
