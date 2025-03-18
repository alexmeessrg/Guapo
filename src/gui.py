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
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, QPushButton, QWidget, QMenuBar, QFrame, QSizePolicy, QTabWidget, QLabel, QTextEdit, QStatusBar
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtCore import Qt, QSize

# Local application imports
from . import styles




class MainWindow(QMainWindow):
    def __init__(self):
    
        super().__init__()

        # Method to create a new button (only called inside the class)
        def _CreateButton(name='',fixedsize=[52,52],iconpath=None,iconsize=[48,48],tooltip=None) -> QPushButton:
            button = QPushButton(name)
            if (tooltip):
                button.setToolTip(tooltip)
            if (iconpath):
                button.setIcon(QIcon(os.path.join(os.path.dirname(__file__), iconpath)))
                button.setIconSize(QSize(iconsize[0],iconsize[1]))
            button.setFixedSize(fixedsize[0], fixedsize[1])
            return button
        
        
        
        
        
        
        # ==== INITIALIZE WINDOW ====
        self.setWindowTitle("Guapo Data Handler")
        self.setGeometry(100, 100, 900, 600)

        # ==== MAIN WIDGET AND LAYOUT ====
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # ==== STATUS BAR =====
        self.status_bar = self.statusBar()
        self.setStatusBar = self.status_bar
        self.status_bar.show()
        self.status_bar.showMessage("Ready")

        # ==== MENUS =====
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

        # === DATA SET READER TAB WIDGETS ===
        read_layout = QVBoxLayout()
        read_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        # Buttons to Add / Delete Data Sets
        self.b_DS_open_tabulated = _CreateButton('Open Tabulated',[192,52],None,[48,48],'Opens CSV, TSV and tabulated data with other delimiters.')
        self.b_DS_open_JSON = _CreateButton('Open JSON',[192,52],None,[48,48],'Opens JSON structured files.')
        self.b_DS_open_SQLite = _CreateButton('Open SQLite',[192,52],None,[48,48],'Opens a local SQLite database.')
        self.b_DS_open_SQL = _CreateButton('Connect to SQL',[192,52],None,[48,48],'Connects to hosted database.')
        self.b_DS_open_XLS = _CreateButton('Open XLS',[192,52],None,[48,48],'Open XLS, XLSX files.')
        self.b_DS_delete = _CreateButton('Delete Data',[192,52],None,[48,48],'Delete loaded data set. Does not delete file.')

        read_layout.addWidget(self.b_DS_open_tabulated)
        read_layout.addWidget(self.b_DS_open_XLS)
        read_layout.addWidget(self.b_DS_open_JSON)
        read_layout.addWidget(self.b_DS_open_SQLite)
        read_layout.addWidget(self.b_DS_open_SQL)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("background-color: #5A5A5A;")  # Optional: Custom color
        separator.setFixedHeight(2)

        read_layout.addWidget(separator)
        read_layout.addWidget(self.b_DS_delete)
        
        # === DATA CLEANING TAB WIDGETS ===
        # === STRING TOOLS  === 
        tools_layout = QVBoxLayout()
        tools_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        # Button for String Operations
        self.b_str_blocked = _CreateButton('Blocked List',[192,52],None,[48,48],'Replaces selected words with ****.')
        self.b_str_dictionary = _CreateButton('Dictionary',[192,52],None,[48,48],'Replaces a list of words by another.')
        self.b_str_statistics = _CreateButton('String Statistics',[192,52],None,[48,48],'Basic statistics for string data.')
        self.b_str_capitalize = _CreateButton('Capitalize',[192,52],None,[48,48],'Sets capitalization rule.')
        self.b_str_duplicates = _CreateButton('Duplicates',[192,52],None,[48,48],'Identify duplicate data.')
        self.b_str_whitespaces = _CreateButton('White Spaces',[192,52],None,[48,48],'Handles whitespace cleaning.')
        self.b_str_breakcolumn = _CreateButton('Split on Delimiter',[192,52],None,[48,48],'Split a data column in 2 or more, acoording to specified delimiter.')
        
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("background-color: #5A5A5A;")  # Optional: Custom color
        separator.setFixedHeight(2)

        tools_layout.addWidget(QLabel('String Operators'))
        tools_layout.addWidget(separator)
        tools_layout.addWidget(self.b_str_whitespaces)
        tools_layout.addWidget(self.b_str_capitalize)
        tools_layout.addWidget(self.b_str_duplicates)
        tools_layout.addWidget(self.b_str_dictionary)   
        tools_layout.addWidget(self.b_str_blocked)   
        tools_layout.addWidget(self.b_str_breakcolumn)
        tools_layout.addWidget(self.b_str_statistics)

        # === SPREADSHEET (TABLE FOR DATA CLEANING) ===
        self.table = QTableWidget(20, 4)  # ROWS X COLUMNS  
        self.table.setSelectionMode(self.table.SelectionMode.ContiguousSelection)  # Allow multiple selections
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectColumns)  # Select full columns
        self.table.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.horizontalHeader().sectionClicked.connect(self.on_column_selected) # event for column selected

        for col in range(self.table.columnCount()):
            self.table.setColumnWidth(col, 100)  # Set fixed width

        # === LOG WINDOW (data modifying log) ===
        self.log_window = QTextEdit(self)
        self.log_window.setReadOnly(True)
        self.log_window.setMaximumWidth(200)
        #set initial values for activity log window -> not necessary later
        html_content = """
        <div>['Country']=> <span style="color: gray;">Capitalize('all')</span></div><div>['Country']=> <span style="color: gray;">Whitespace remove('double')</span></div><div>['Area']=> <span style="color: gray;">Numeric scale('0.001')</span></div>
        """          
        self.log_window.setText(html_content)



        # ==== TAB SWITCHER ====
        self.side_tab = QTabWidget()
        self.side_tab.setTabPosition(QTabWidget.TabPosition.West)

        tab1 = QWidget() #on this tab will be all the widgets to load data sets from different formats
        tab1_layout = QVBoxLayout()
        tab1_layout.addLayout(read_layout)
        tab1.setLayout(tab1_layout)

        tab2 = QWidget() #on this tab will be all the widgets for data cleaning
        tab2_layout = QHBoxLayout()
        tab2_layout.addLayout(tools_layout)
        tab2_layout.addWidget(self.table) #spreadsheet for data
        tab2_layout.addWidget(self.log_window) #operations log window
        tab2.setLayout(tab2_layout)

        tab3 = QWidget() #on this tab will be all the widgets for analysis
        tab3_layout = QVBoxLayout()
        tab3_layout.addWidget(QLabel("Analysis"))
        tab3.setLayout(tab3_layout)

        tab4 = QWidget() #on this tab will all the widgets for visualization
        tab4_layout = QVBoxLayout()
        tab4_layout.addWidget(QLabel("Visualization"))
        tab4.setLayout(tab4_layout)

        self.side_tab.addTab(tab1, "Data Sets")
        self.side_tab.addTab(tab2, "Cleaning")
        self.side_tab.addTab(tab3, "Analysis")
        self.side_tab.addTab(tab4, "Visualization")
        


        # === Add Widgets to Main Layout ===       
        main_layout.addWidget(self.side_tab)      

        # === Apply StyleSheet ===
        self.setStyleSheet(styles.GUIStyles.style_sheet)

    
    
    def on_column_selected(self, column: int): #this will trigger when a column header is selected, updating the bottom Status Bar and Activity log 
        header_item = self.table.horizontalHeaderItem(column)
        if (header_item):
            self.table.selectColumn(column)  # Ensure the column gets fully selected
            column_name = header_item.text()
            self.status_bar.showMessage(f"Selected Column {column} - '{column_name}'")
            self.status_bar.show()
            print(self.log_window.toPlainText())
            self.log_window.setHtml(f"""{self.log_window.toHtml()}<div>Selected Column <span style="color: gray;">{column} - '{column_name}'</span></div>""")

    
    # this methods will be called from outside the class to update visuals and data     
    def set_event_handlers(self, target, function): #use this to add main.py functions to the GUI buttons.
        match target:
            case "table":
                self.table.selectionModel().selectionChanged.connect(function) #add the 'normal' event handler and additionally another one.
            case "b_str_blocked":
                self.b_str_blocked.clicked.connect(function)
            case "b_str_whitespace":
                self.b_str_whitespaces.clicked.connect(function)
    
    def set_headers(self,headers): #set the headers for a spreadsheet
        self.table.setHorizontalHeaderLabels(headers)

    def set_data_table(self,data): #set the data table values
        for row, rowData in enumerate(data):
            for col, value in enumerate(rowData):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))
