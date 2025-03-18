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
    transition: all 0.2s ease-in-out;
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
    border: 1px solid #34495E;
    gridline-color: #4A637D;
    selection-background-color: #1F618D;
    border-radius: 6px;
}

QHeaderView::section {
    background: #34495E;
    padding: 0px 10px;
    border: none;
    font-size: 10pt;
    color: #BDC3C7;
    border-radius: 6px;
}

/* === QPushButton (Modern Buttons) === */
QPushButton {
    background: linear-gradient(to bottom, #1F618D, #154360);
    color: white;
    border: none;
    padding: 10px 15px;
    border-radius: 6px;
    font-size: 12pt;
    transition: all 0.3s ease-in-out;
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

/* === QFrame (Modern Section Containers) === */
QFrame {
    background: #2C3E50;
    border-radius: 8px;
    border: 0px solid #34495E;
    padding: 10px;
}

/* === QMenuBar (Modern Menu Bar) === */
QMenuBar {
    background: #2C3E50;
    padding: 6px;
    border-bottom: 2px solid #34495E;
}

QMenuBar::item {
    padding: 8px 12px;
    background: transparent;
    border-radius: 6px;
    color: #BDC3C7;
}

QMenuBar::item:selected {
    background: #1F618D;
    color: #FFFFFF;
}

/* === QMenu (Modern Dropdown Menus) === */
QMenu {
    background: #2C3E50;
    border: 1px solid #34495E;
    border-radius: 6px;
}

QMenu::item {
    padding: 8px 15px;
    border-radius: 4px;
    color: #BDC3C7;
}

QMenu::item:selected {
    background: #1F618D;
    color: #FFFFFF;
}

/* === QMenu Disabled Items === */
QMenu::item:disabled {
    color: #4A637D;
}
"""



    dark_grey_style = """
    /* QFrame Styling */
    QFrame {
        background-color: #555555;  /* Dark Grey */
        border: 0px solid #444;  
        border-radius: 10px;
        padding: 0px;
    }

    /* QPushButton Default (Transparent) */
    QPushButton {
        background-color: transparent;
        border: none;
        color: white;  /* White text for visibility */
        text-align: left;
        padding-left:5px;
        font-size: 14px;
        padding: 5px;
    }

    /* QPushButton Hovered */
    QPushButton:hover {
        background-color: rgba(45, 45, 45, 0.9); 
        border-radius: 5px;
    }

    /* QPushButton Pressed (Clicked) */
    QPushButton:pressed {
        background-color: rgba(255, 255, 255, 0.2);
    }

    /* QPushButton Disabled */
    QPushButton:disabled {
        color: gray;  /* Greyed out text */
        background-color: transparent;
        border: none;
    }
"""


    @classmethod
    def Change_Global_Style(cls, style_type): #later use this method to update the used style.
        pass
    