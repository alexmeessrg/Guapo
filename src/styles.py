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
/* === Global Styling === */
QWidget {
    background-color: #1E252D;
    font-family: 'Segoe UI', Arial, sans-serif;
    font-size: 12pt;
    color: #E0E0E0;
}
/* === QTabWidget === */
QTabWidget::pane {
    border: 1px solid #34495E;
    background: #2C3E50;
    border-radius: 6px;
}
QTabBar::tab {
    background: #34495E;
    border: 1px solid #2C3E50;
    padding: 10px 8px;
    margin: 2px;
    border-radius: 6px;
    color: #BDC3C7;
}
QTabBar::tab:selected {
    background: #1F618D;
    border: 2px solid #3498DB;
    color: #FFFFFF;
    font-weight: bold;
}
/* === QTableWidget (Modern Table) === */
QTableWidget {
    background: #2C3E50;
    alternate-background-color: #2685a5;
    border: 1px solid #34495E;
    gridline-color: #4A637D;
    selection-background-color: #1F618D;
    border-radius: 6px;
    text-align: center;
    font-size: 10x;
}
QTableWidget::item {
    color: cyan;
    font-size: 8px;

}
QHeaderView::section {
    background: #34495E;
    padding: 0px;
    border: none;
    font-size: 10pt;
    color: #BDC3C7;
    border-radius: 6px;
    text-align: center;
    border: 1px solid #3498DB
}
/* === QPushButton (Modern Buttons) === */
QPushButton {
    background: rgba(128, 128, 128, 16);;
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 6px;
    font-size: 12pt;
}
QPushButton:hover {
    background: linear-gradient(to bottom, #2980B9, #1F618D);
    border: 2px solid #454545
}
QPushButton:pressed {
    background: linear-gradient(to bottom, #154360, #0E374A);
}
QPushButton:disabled {
    background: #2C3E50;
    color: #7F8C8D;
}
QTextEdit {
    font-family: Arial;
    font-size: 12x;
    padding: 2x;
    border-radius: 5px;
}
"""

    small_button = """
QPushButton {
    background: rgba(128, 128, 128, 16);;
    color: white;
    border: none;
    padding: 0px 0px;
    border-radius: 4px;
    font-size: 12pt;
}
QPushButton:hover {
    background: linear-gradient(to bottom, #2980B9, #1F618D);
    border: 2px solid #454545
}
QPushButton:pressed {
    background: linear-gradient(to bottom, #154360, #0E374A);
}
QPushButton:disabled {
    background: #2C3E50;
    color: #7F8C8D;
}
"""



    @classmethod
    def Change_Global_Style(cls, style_type): #later use this method to update the used style.
        pass
    