"""
File: styles.py
Author: Alex Mees
Date: 2025-03-16
Description: GUI styles
License: MIT
"""
# Standard library imports

# Third-party imports

# Local application imports

class GUIStyles():  

    style_sheet = """
/* ========== MAIN WINDOW ========== */
QMainWindow {
    background-color: #e3f2fd; /* Light Blue Background */
}

/* ========== MENU BAR ========== */
QMenuBar {
    background-color: #ffffff;
    color: #333;
    font-size: 14px;
    padding: 5px;
    border-bottom: 1px solid #b0bec5;
}
QMenuBar::item {
    background: transparent;
    padding: 8px 15px;
    margin: 2px;
}
QMenuBar::item:selected {
    background: #bbdefb;
}
QMenuBar::item:pressed {
    background: #90caf9;
}

/* ========== MENU DROPDOWN ========== */
QMenu {
    background-color: #ffffff;
    color: #333;
    border: 1px solid #b0bec5;
}
QMenu::item {
    padding: 8px 15px;
    border-radius: 3px;
}
QMenu::item:selected {
    background-color: #bbdefb;
}
QMenu::separator {
    height: 1px;
    background: #b0bec5;
    margin: 5px 0;
}

/* ========== BUTTONS ========== */
QPushButton {
    background-color: #1976d2;
    color: white;
    font-size: 14px;
    border-radius: 4px;
    padding: 8px 15px;
    border: 0px solid #1565c0;
}
QPushButton:hover {
    background-color: #1565c0;
}
QPushButton:pressed {
    background-color: #0d47a1;
}
QPushButton:disabled {
    background-color: #e6e6e6;
    color: #aaa;
}

/* ========== TABLE WIDGET ========== */
QTableWidget {
    background-color: #ffffff;
    border: 1px solid #b0bec5;
    gridline-color: #b0bec5;
    font-size: 14px;
}
QHeaderView::section {
    background-color: #e3f2fd;
    color: #333;
    padding: 6px;
    border: 1px solid #b0bec5;
    font-weight: bold;
}
QTableWidget::item {
    padding: 8px;
}
QTableWidget::item:selected {
    background-color: #bbdefb;
    color: #000;
}

/* ========== WIDGET CONTAINER ========== */
QWidget {
    background-color: #e3f2fd;
    color: #333;
    font-size: 14px;
}

/* ========== SCROLLBAR ========== */
QScrollBar:vertical {
    border: none;
    background: #e3f2fd;
    width: 10px;
    margin: 0px;
}
QScrollBar::handle:vertical {
    background: #90caf9;
    border-radius: 5px;
    min-height: 20px;
}
QScrollBar::handle:vertical:hover {
    background: #64b5f6;
}
QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {
    background: none;
    height: 0px;
}
"""
    
    @classmethod
    def Change_Global_Style(cls, style_type): #later use this method to update the used style.
        pass
    