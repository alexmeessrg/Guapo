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
from typing import Tuple

# Third-party imports
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QWidget, QMenuBar, QFrame, QSizePolicy, QTabWidget, QLabel, QTextEdit, 
                             QStatusBar, QStackedWidget, QRadioButton, QButtonGroup, QComboBox, QScrollArea, QFileDialog,
                             QDialog)
from PyQt6.QtGui import QAction, QIcon, QPalette, QColor
from PyQt6.QtCore import Qt, QSize, pyqtSignal

import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas

# Local application imports
from . import styles
from .data_format import DataType

class DataSetItem(QWidget):
    "A class to create a data set item with widget controls."
    def __init__(self, data_set_name='',item_index = 0, headers=None, data_type: list[DataType]=None, parent=None):
        super().__init__()

        self.parent = parent
        self.index = item_index

        self.setWindowTitle(data_set_name)
        self.setGeometry(0,0,200,100)
        self.setMinimumWidth(400)
        self.setMaximumHeight(150)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.data_type = data_type
        
        wrapper1 = QWidget()
        wrapper1.setStyleSheet("background-color: #2C3E50; border: 0px; border-radius: 6px; font-weight: bold;")
        wrapper1.setFixedHeight(40)
        
        row1 = QHBoxLayout(wrapper1)
        row1.addWidget(QLabel(data_set_name))
        row1.addWidget(QLabel('Tools'))

        wrapper2 = QWidget()
        wrapper2.setStyleSheet("background-color: transparent; border: 0px solid black;")
        wrapper2.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Minimum)
        row2 = QHBoxLayout(wrapper2)
        
        type_names = [member.name.capitalize() for member in DataType]

        for index, header in enumerate(headers): #add a column to each 
            inner_wrapper = QWidget()
            inner_wrapper.setStyleSheet("background-color: #2685a5; border: 1px solid #4da8c6; border-radius: 4px;")
            inner_wrapper.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Expanding)
            row3 = QVBoxLayout(inner_wrapper)

            header_label = QLabel(f'{header}')
            header_label.setStyleSheet("font-weight: bold; text-align: center;")
            header_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            row3.addWidget(header_label)
            
            type_dropdown = QComboBox()
            type_dropdown.addItems(type_names)
            type_dropdown.setCurrentText(str(self.data_type[index]).capitalize())
            type_dropdown.col_index = index
            type_dropdown.currentIndexChanged.connect(lambda index:self.change_col_datatype(index)) #send the index of the selected item to the function (the change in data type)
            
            row3.addWidget(type_dropdown)
            row2.addWidget(inner_wrapper)

        layout.addWidget(wrapper1, alignment=Qt.AlignmentFlag.AlignTop)
        layout.addWidget(wrapper2, alignment=Qt.AlignmentFlag.AlignTop)

        
        
    def change_col_datatype(self, datatype_index=0):
        col_index = self.sender().col_index
        if not (str(self.data_type[col_index]).capitalize() == self.sender().currentText().capitalize()): #only operate if current selection is different from existing type selection
            if (self.parent.change_data_col_data_type(self.index, col_index, DataType(datatype_index+1), new_dataformat='')): #index of the dataset, index of the column, the attempted data type change, a format string #ENUM is 1 based!
                
                self.data_type[col_index] = DataType(datatype_index+1) #if conversion successful update list of data_types

            else: 
                self.sender().setCurrentText(str(self.data_type[col_index]).capitalize()) #if conversion unsuccessful return QComboBox to previous value.



class MainWindow(QMainWindow):
    def __init__(self, main):
        super().__init__()

        self.main = main #reference for the main method, to access its methods.
        self.main.print_something()

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
        
        # Class Variables
        self.dataset_column_index = int(-1) #which column was selected on click
        

        
        
        # ==== INITIALIZE WINDOW ====
        self.setWindowTitle("Guapo Data Handler")
        self.setGeometry(100, 100, 1200, 900)

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
        read_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # === ADD/DELETE DATA SET === (first tab)
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

        self.data_set_item_layout = QVBoxLayout() #layout for the list of loaded data sets
        self.data_set_item_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

       
        # === DATA CLEANING TAB WIDGETS === (second tab)
        # === STRING TOOLS  === 
        self.str_tools_layout = QVBoxLayout()
        self.str_tools_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        # Button for String Operations
        self.b_str_blocked = _CreateButton('Blocked List',[192,52],None,[48,48],'Replaces selected words with ****.')
        self.b_str_dictionary = _CreateButton('Dictionary',[192,52],None,[48,48],'Replaces a list of words by another.')
        self.b_str_statistics = _CreateButton('String Statistics',[192,52],None,[48,48],'Basic statistics for string data.')
        self.b_str_capitalize = _CreateButton('Capitalize',[192,52],None,[48,48],'Sets capitalization rule.')
        self.b_str_duplicates = _CreateButton('Duplicates',[192,52],None,[48,48],'Identify duplicate data.')
        self.b_str_whitespaces = _CreateButton('White Spaces',[192,52],None,[48,48],'Handles whitespace cleaning.')
        self.b_str_breakcolumn = _CreateButton('Split on Delimiter',[192,52],None,[48,48],'Split a data column in 2 or more, acoording to specified delimiter.')
        
        #Combo boxes
        #Capitalize
        self.cb_str_combo1 = QComboBox()
        self.cb_str_combo1.addItems(['ALL CAPS','Each Word','First word','lowercase','iNVERT'])
        self.cb_str_combo1.setCurrentIndex(0)

        #White spaces
        self.cb_str_combo2 = QComboBox()
        self.cb_str_combo2.addItems(['Trailing','Leading','Leading+Trailing','Double space','All the above'])
        self.cb_str_combo2.setCurrentIndex(0)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("background-color: #5A5A5A;")  # Optional: Custom color
        separator.setFixedHeight(2)

        self.str_tools_layout.addWidget(QLabel('String Operators'))
        self.str_tools_layout.addWidget(separator)
        self.str_tools_layout.addWidget(self.b_str_whitespaces)
        self.str_tools_layout.addWidget(self.cb_str_combo2)
        self.str_tools_layout.addWidget(self.b_str_capitalize)
        self.str_tools_layout.addWidget(self.cb_str_combo1)
        self.str_tools_layout.addWidget(self.b_str_duplicates)
        self.str_tools_layout.addWidget(self.b_str_dictionary)   
        self.str_tools_layout.addWidget(self.b_str_blocked)   
        self.str_tools_layout.addWidget(self.b_str_breakcolumn)
        self.str_tools_layout.addWidget(self.b_str_statistics)

        # === NUMERIC DATA TOOLS === 
        # NUMERIC OPERATIONS TO CODE: OFFSET(SUBTRACT/ADD), SCALE (MULTIPLY/DIVIDE), LOGARITMIC SCALE, CLAMP (SET MIN/MAX), CONVERT (INT=>FLOAT OR FLOT=>INT)
        # MISSING VALUES RULES: LOCAL AVERAGE, GLOBAL AVERAGE, NaN, FIXED VALUE
        # OUTLIER HANDLING RULES: CLAMP BEYOND RANGE (FIXED RANGES, STD RANGES), CHECK MAX DELTA
        # STATISTICS: MEAN, MEDIAN, MODE, STANDARD DEVIATION, SKEWNESS, KURTOSIS, LENGTH
        
        self.num_tools_layout = QVBoxLayout()
        self.num_tools_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        
        #Buttons for numeric operations
        self.b_num_offset = _CreateButton('Offset Values',[192,52],None,[48,48],'Add/subtract to values. Does NOT change numeric type (INT/FLOAT). INT will be round to nearest integer.')
        self.b_num_scale = _CreateButton('Scale Values',[192,52],None,[48,48],'Multiply values by this amount. Does NOT change numeric type (INT/FLOAT). INT will be round to nearest integer.')
        self.b_num_logscale = _CreateButton('Log Scale Values',[192,52],None,[48,48],'Transform to the LOG10 equivalent. Does NOT change numeric type (INT/FLOAT). INT will be round to nearest integer.')
        self.b_num_clamp = _CreateButton('Clamp Values',[192,52],None,[48,48],'Clamp Values to MIN/MAX. Does NOT change numeric type (INT/FLOAT). INT will be round to nearest integer.')
        self.b_num_convert_to_float = _CreateButton('Int=>Float',[192,52],None,[48,48],'Convert data type from integer to float (decimal) values.')
        self.b_num_convert_to_integer = _CreateButton('Float=>Int',[192,52],None,[48,48],'Convert data type from float (decimal) to integer. INT will be round to nearest integer.')

        #Add buttons to layout
        self.num_tools_layout.addWidget(QLabel('Numeric Data Operators'))
        self.num_tools_layout.addWidget(separator)
        self.num_tools_layout.addWidget(self.b_num_offset)
        self.num_tools_layout.addWidget(self.b_num_scale)
        self.num_tools_layout.addWidget(self.b_num_logscale)
        self.num_tools_layout.addWidget(self.b_num_clamp)
        self.num_tools_layout.addWidget(self.b_num_convert_to_float)
        self.num_tools_layout.addWidget(self.b_num_convert_to_integer)

        


        # === DATE DATA TOOLS ===
        # DATE OPERATIONS: CHANGE DATA FORMAT, OFFSET DAYS (SUBTRACT/ADD)
        # MISSING VALUES RULES: FILL DATE GAP, FIXED VALUE


        # === TIME DATA (short or non day-reference time) TOOLS ===



        # === GEOSPATIAL DATA TOOLS ===


        # === BOOLEAN DATA TOOLS ===
        

        # === Cleaning Tools Tab Switcher === ADD ALL CATEGORIES OF CLEANING TOOLS HERE
        self.clean_tools_tab = QStackedWidget() #this tab switcher will change active tab depending on what table column is active, so it needs to accesible outside the class.

        # individual tools tab layout
        clean_tab1 = QWidget() #on this tab will be the numeric data cleaning tools
        clean_tab1.setLayout(self.num_tools_layout)
        
        clean_tab2 = QWidget() #on this tab will be the numeric data cleaning tools
        clean_tab2.setLayout(self.str_tools_layout)

        # ... add more here

        #all all subtabs to tabwidget
        self.clean_tools_tab.addWidget(clean_tab1)
        self.clean_tools_tab.addWidget(clean_tab2)
        self.clean_tools_tab.setMaximumWidth(200)
        self.clean_tools_tab.setCurrentIndex(1) #TODO: just for quick testing
        # ... add more here

        

        # === SPREADSHEET (TABLE FOR DATA CLEANING) ===
        self.table = QTableWidget(20, 4)  # ROWS X COLUMNS  
        self.table.setSelectionMode(self.table.SelectionMode.ContiguousSelection)  # Allow multiple selections
        self.table.setSelectionBehavior(self.table.SelectionBehavior.SelectColumns)  # Select full columns
        self.table.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().sectionClicked.connect(self.on_column_selected) # event for column selected

        for col in range(self.table.columnCount()):
            self.table.setColumnWidth(col, 100)  # Set fixed width

        # === LOG WINDOW (data modifying log) ===
        self.log_window = QTextEdit(self)
        self.log_window.setReadOnly(True)
        self.log_window.setMaximumWidth(200)
        #set initial values for activity log window -> NOT NECESSARY LATER
        html_content = """
        <div>['Country']=> <span style="color: gray;">Capitalize('all')</span></div><div>['Country']=> <span style="color: gray;">Whitespace remove('double')</span></div><div>['Area']=> <span style="color: gray;">Numeric scale('0.001')</span></div>
        """          
        self.log_window.setText(html_content)


        # VISUALIZATION TOOLS
        

        # Graph Window
        self.canvas = FigureCanvas(plt.figure(figsize=(6,4)))

        #Data Columns Selector
        # Scroll Area Setup
        self.dataset_scroll_area = QScrollArea(self)
        self.dataset_scroll_area.setWidgetResizable(True)
        self.dataset_scroll_area.setMaximumWidth(200)
        # Main container widget
        self.dataset_container = QWidget()       
        self.current_data_list = QVBoxLayout()
        self.dataset_scroll_area.setWidget(self.dataset_container)
        self.dataset_container.setLayout(self.current_data_list)

        for x in range(15):
            self.populate_dataset_selection(f'Button: {x}') #add just for testing (each button is a graph type)


        # ==== TAB SWITCHER ====
        self.side_tab = QTabWidget()
        self.side_tab.setTabPosition(QTabWidget.TabPosition.West)

        tab1 = QWidget() #on this tab will be all the widgets to load data sets from different formats
        tab1_layout = QHBoxLayout()
        tab1_layout.addLayout(read_layout)
        tab1_layout.addLayout(self.data_set_item_layout)
        tab1.setLayout(tab1_layout)

        tab2 = QWidget() #on this tab will be all the widgets for data cleaning
        tab2_layout = QHBoxLayout()
        tab2_layout.addWidget(self.clean_tools_tab) #this includes tools tab for each individual type of data.
        tab2_layout.addWidget(self.table) #spreadsheet for data
        tab2_layout.addWidget(self.log_window) #operations log window
        tab2.setLayout(tab2_layout)

        tab3 = QWidget() #on this tab will be all the widgets for analysis
        tab3_layout = QHBoxLayout()
        tab3_layout.addWidget(self.dataset_scroll_area) #the selector for columns using the current data set.
        tab3_layout.addWidget(self.canvas)
        self.plot_seaborn() #actually draw the graph #TODO: remove later
        tab3.setLayout(tab3_layout)

        tab4 = QWidget() #on this tab will all the widgets for visualization
        tab4_layout = QHBoxLayout()
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
    
    # Method to update the status bar
    def update_statusbar(self, message=''):
            if (message):
                self.status_bar.showMessage(message)
                self.status_bar.show()
    """
    === Method to update log window ===
        = Message Type Conventions =
        messagetype: 'str_capitalization'
            message: [Column Name, Column Index, Capitalization Format]
        messagetype: 'str_whitespace'
            message: [Column Name, Column Index, Whitespace Removal Format]
        messagetype: 'str_blocked'
            message: xxxx
        messagetype? 'str_dictionary

    """
    def add_to_log(self, message=[], messagetype=''): #message arguments and how to format it by type
        formated_message = ''      
        try:
            match messagetype:
                case 'str_capitalization':
                    formated_message = f"""<div>Capitalization rule: <span style="color: gray;">Col: {message[0]}[{message[1]}] - Rule: {message[2]}</span></div>"""
                case 'str_whitespace':
                    formated_message = f"""<div>Whitespace removed: <span style="color: gray;">Col: {message[0]}[{message[1]}] - Rule: {message[2]}</span></div>"""
                case 'str_blocked':
                    formated_message = f"""<div>Blocked words removed <span style="color: gray;">Col: {message[0]}[{message[1]}] - Used Custom List?: {message[2]}</span></div>"""
                case 'str_dictionary':
                    formated_message = f"""<div>Dictionary words applied <span style="color: gray;">Col: {message[0]}[{message[1]}] - Number of Changes: {message[2]}</span></div>"""
                case _:
                    formated_message = '[ERROR] File "gui.py", Function "add_to_log", Bad message type.'
                    raise ValueError

            self.log_window.setHtml(f"""{self.log_window.toHtml()}{formated_message}""")

        except IndexError:
            formated_message = '[ERROR] File "gui.py", Function "add_to_log", Message index error.'
        except ValueError:
            formated_message = '[ERROR] File "gui.py", Function "add_to_log", Bad message log type error.'
        except:
            formated_message = '[ERROR] File "gui.py", Function "add_to_log", Unknown error.'
            self.update_statusbar(formated_message)



    
    def on_column_selected(self, column: int): #this will trigger when a column header is selected, updating the bottom Status Bar and Activity log 
        header_item = self.table.horizontalHeaderItem(column)
        if (header_item):
            self.table.selectColumn(column)  # Ensure the column gets fully selected
            self.dataset_column_index = column
            column_name = header_item.text()
            self.status_bar.showMessage(f"Selected Column {column} - '{column_name}'")
            self.status_bar.show()
            self.log_window.setHtml(f"""{self.log_window.toHtml()}<div>Selected Column <span style="color: gray;">{column} - '{column_name}'</span></div>""")
            # tool bar to select
            type = self.main.return_col_type(0, column)
            match type:
                case DataType.TEXT:
                    self.clean_tools_tab.setCurrentIndex(1)
                case DataType.INTEGER:
                    self.clean_tools_tab.setCurrentIndex(0)
                case DataType.FLOAT:
                    self.clean_tools_tab.setCurrentIndex(0)
                case _:
                    pass
             #TODO: JUST FOR TESTING REMOVE

    
    def b_connect_whitespace(self,option='doubles'):
        self.main.baction_str_whitespace()
    
    
    
    
    # this methods will be called from outside the class to update visuals and data     
    def set_event_handlers(self, target, function): #use this to add main.py functions to the GUI buttons.
        match target:
            case "table":
                self.table.selectionModel().selectionChanged.connect(function) #add the 'normal' event handler and additionally another one.
            case "b_str_blocked":
                self.b_str_blocked.clicked.connect(function)
            case "b_str_whitespace":
                self.b_str_whitespaces.clicked.connect(function)
    
    def click_event_handlers(self, target, function): #use this to add main.py functions to the GUI buttons.
        target.clicked.connect(function)


    
    def set_headers(self,headers): #set the headers for a spreadsheet
        self.table.setHorizontalHeaderLabels(headers)

    def set_data_table(self,data): #set the data table values
        for row, rowData in enumerate(data):
            for col, value in enumerate(rowData):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def plot_seaborn(self):
        """Generate a Seaborn plot and display it in the PyQt6 window."""
        sns.set_style("darkgrid")

        # Load example dataset
        tips = sns.load_dataset("tips")

        # Create a Matplotlib figure
        fig, ax = plt.subplots(figsize=(6,4))
        ax.set_title("Custom Title")
        ax.set_ylabel("Y-axis Label")
        sns.scatterplot(x="total_bill", y="tip", data=tips, ax=ax)

        # Draw the plot on the canvas
        self.canvas.figure = fig
        self.canvas.draw()

    def change_data_col_data_type(self, dataset_index=-1, dataframe_column=-1, new_datatype=DataType.TEXT, new_dataformat='')-> bool:
        result = self.main.update_dataframe_column(dataset_index, dataframe_column, new_datatype, new_dataformat)

        return result
    
    def add_dataset_item_entry(self, data_set_name: str='Data Set', item_index: int=0, headers: list[str]=[''], data_types: list[DataType]=None):
        dataset_item = DataSetItem(data_set_name, item_index, headers, data_types, self)
        dataset_item.setSizePolicy(QSizePolicy.Policy.Expanding,QSizePolicy.Policy.Minimum)
        self.data_set_item_layout.addWidget(dataset_item)
        print("Item added")




    def populate_dataset_selection(self,item_name): #use to create the list of data assets
        self.current_data_list.addWidget(QPushButton(item_name))

    def clear_layout(self, layout): #clear layouts recursively
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
            else:
                self.clear_layout(item.layout())



                    

        
