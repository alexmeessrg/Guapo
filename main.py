"""
File: main.py
Author: Alex Mees
Date: 2025-03-13
Description: Entry point for Project Guapo.
License: MIT

Basic Workflow
1) Load data by type
2) Handle data type
3) Add to a data set list
4) From selected data set, do data cleaning
5) Display results
6) Export graphs or write/overwrite consolidated data set.

"""

# Standard library imports

# Third-party imports
import pandas as pd

# Local application imports
from src.fetcher import *
from src.wrangler import *
from src.gui import *
from src.data_format import *

class main:
    def __init__(self):
        # === WINDOW INITIALIZATION ===
        self.app = QApplication(sys.argv) #initializes the application with command line support
        self.window = MainWindow(self) #store a reference to self to access main functions. #if worried about memory leak you can use [weakref.proxy(self)]
        self.window.show()

        # === MAIN VARIABLES SETUP ===
        self.block_execution = False #set to wait till operation is over to allow processes
        self.active_directory = '' #the directory the file open dialog will be pointed at initially
        
        self.use_custom_blocked_list = False #which blocked word list to use

        self.use_custom_dictionary = False #use a custom dictionary for word replacement
        self.custom_dictionaries = [[''],['']] #the custom dictionaries to use
        self.active_custom_dictionary = [''] #the active custom dictionary
        
        self.current_dataset_index = -1
        self.datasets: list[TableFormat] = [] #this holds all the data sets loaded by the system. [Limit size?]
        self.connect_all_functions()
        
        #Pre-GUI test
        print("xxxxxxx Doing tests here xxxxxxxx")
    
        data, data_types, delimiter, has_header, error = self.open_CSV("E:/GUAPO/guapo/sample/sampleCSVdata.txt")
    
        if not (error):
            pass
            #for testing TODO:remove
            #self.datasets.append(TableFormat(DataMode.TABLE, dtype=[DataType.TEXT,DataType.INTEGER,DataType.INTEGER,DataType.TEXT],dformat=[], dheaders=data.columns.to_list(),data=data))
            #self.current_dataset_index = len(self.datasets) + 1

            
            #self.thisdata = TableFormat(DataMode.TABLE, dtype=[DataType.TEXT,DataType.INTEGER,DataType.INTEGER,DataType.TEXT],dformat=[], dheaders=data.columns.to_list(),data=data)

             #this depends on having an existing self.thisdata -> this hard dependency must be removed.


            #self.thisdata.search_result(0,'S')
            #self.window.set_headers(['Country','Area','Population','Capital'])
            #self.window.set_data_table(self.thisdata.data.values.tolist())
        else:
            print(error)
    
        sys.exit(self.app.exec()) #putting this here so it won't block the rest of the commands.

    
    # ==== Open Files by Types ====
    def open_CSV(self,file_path) -> Tuple [pd.DataFrame,list[DataType], str, bool, str]:
        """
        Initialize file opening and data handling for CSV

        Args:
        file_path (str) = full file path

        Outputs:
        DataFrame = the dataframe of the processed data set
        list[DataType] = the Data Types enum for the data set
        str = the delimiter
        bool = if data has delimiter
        str = the error string
        """
        raw_data, error = Fetcher.read_CSV(file_path)
        if not (error):
            data, data_types, delimiter, has_header, error = Wrangler.handle_tabulated(raw_data) #this take the raw text data and process it
            if not (error):
                return data, data_types, delimiter, has_header, error
            else:
                return None, None, None, None, error   
        else:
            return None, None, None, None, error
        
    def open_SQLite(self,file_path):
        """
        Initialize data connection and data handling for SQL

        Args:
        file_path (str) = full file path
        """
        #"E:/GUAPO/guapo/sample/sampleSQL.db"
        Fetcher.read_SQLite(file_path) #TODO: replace with proper file path



    # ==== GUI initialization scripts ====
    # === Actions for GUI buttons ===

    # == Method for removing whitespace
    def baction_str_whitespace(self):
        """
        Button connected action for white space removal method
        """
        try:
            col_index = self.window.dataset_column_index
            option = 'all'
            match self.window.cb_str_combo2.currentIndex():
                case 0:
                    capitalization_option = 'trailing'
                case 1:
                    capitalization_option = 'leading'
                case 2:
                    capitalization_option = 'both'
                case 3:
                    capitalization_option = 'doubles'
                case 4:
                    capitalization_option = 'all'
                case _:
                    raise ValueError
            
            self.datasets[self.current_dataset_index].remove_whitespace(col_index, option)
            self.window.set_data_table(self.datasets[self.current_dataset_index].data.values.tolist())
            self.window.add_to_log([self.datasets[self.current_dataset_index].data.columns[col_index], col_index, option],'str_whitespace')
            self.window.update_statusbar('Whitespace removal Operation')
                    
        except IndexError:
            self.window.update_statusbar('[ERROR] File "main.py", Function "baction_str_whitespace", Wrong data column index.')
        except ValueError:
            self.window.update_statusbar('[ERROR] File "main.py", Function "baction_str_whitespace", Wrong method option.')
        except:
            self.window.update_statusbar('[ERROR] File "main.py", Function "baction_str_whitespace", Unknown error.')


        if not (self.window.dataset_column_index < 0):
            self.datasets[self.current_dataset_index].remove_whitespace(self.window.dataset_column_index,'doubles')
            self.window.set_data_table(self.datasets[self.current_dataset_index].data.values.tolist())
            #print(self.datasets[self.current_dataset_index].data.iloc[:,self.window.dataset_column_index].to_list())
    
    # == Method for capitalization rule
    def baction_str_capitalization(self):
        """
        Button connected action for capitalization method
        """
        try:
            col_index = self.window.dataset_column_index
            option = 'all' #the capitalization rule option
            match self.window.cb_str_combo2.currentIndex():
                case 0:
                    option = 'all'
                case 1:
                    option = 'each'
                case 2:
                    option = 'first'
                case 3:
                    option = 'lowercase'
                case 4:
                    option = 'invert'   
                case _:
                    raise ValueError
            
            self.datasets[self.current_dataset_index].capitalization_rule(col_index, option)
            self.window.set_data_table(self.datasets[self.current_dataset_index].data.values.tolist())
            self.window.add_to_log([self.datasets[self.current_dataset_index].columns[col_index], col_index, option],'str_capitalization')
            self.window.update_statusbar('Capitalization Operation')
                    
        except IndexError:
            self.window.update_statusbar('[ERROR] File "main.py", Function "baction_str_capitalization", Wrong data column index.')
        except ValueError:
            self.window.update_statusbar('[ERROR] File "main.py", Function "baction_str_capitalization", Wrong method option.')
        except:
            self.window.update_statusbar('[ERROR] File "main.py", Function "baction_str_capitalization", Unknown error.')

    # == Method for blocked words rule
    def baction_str_blocked_words(self):
        """
        Button connected action for blocked words replace method
        """
        try:
            col_index = self.window.dataset_column_index
            if (self.use_custom_blocked_list):
                #implement this later
                blocked_words_list = ''
                pass
            else:
                blocked_words_list = constants.BLOCKED_WORD_LIST #user should be able to review these TODO:add option to add own list
            
            self.datasets[self.current_dataset_index].blocked_words(col_index, blocked_words_list)
            self.window.set_data_table(self.datasets[self.current_dataset_index].data.values.tolist())
            self.window.add_to_log([self.datasets[self.current_dataset_index].data.columns[col_index], col_index, self.use_custom_blocked_list],'str_blocked')
            self.window.update_statusbar('Blocked word Operation')
                    
        except IndexError:
            self.window.update_statusbar('[ERROR] File "main.py", Function "baction_str_blocked_word", Wrong data column index.')
        except ValueError:
            self.window.update_statusbar('[ERROR] File "main.py", Function "baction_str_blocked_word", Wrong method option.')
        except:
            self.window.update_statusbar('[ERROR] File "main.py", Function "baction_str_blocked_word", Unknown error.')

    # == Method for dictionary words replacement
    def baction_str_dictionary_words(self):
        """
        Button connected action for dictionary replace method
        """
        try:
            col_index = self.window.dataset_column_index
            if (self.use_custom_dictionary):
                #implement this later
                dictionary = self.active_custom_dictionary
                pass
            else:
                dictionary = constants.COMMON_DICTIONARY_REPLACEMENTS
            
            self.datasets[self.current_dataset_index].dictionary_words(col_index, dictionary)
            self.window.set_data_table(self.datasets[self.current_dataset_index].data.values.tolist())
            self.window.add_to_log([self.datasets[self.current_dataset_index].data.columns[col_index], col_index, self.use_custom_dictionary],'str_dictionary')
            self.window.update_statusbar('Blocked word Operation')
                    
        except IndexError:
            self.window.update_statusbar('[ERROR] File "main.py", Function "baction_str_blocked_word", Wrong data column index.')
        except ValueError:
            self.window.update_statusbar('[ERROR] File "main.py", Function "baction_str_blocked_word", Wrong method option.')
        except:
            self.window.update_statusbar('[ERROR] File "main.py", Function "baction_str_blocked_word", Unknown error.')        


    #load tabulated data button click
    def get_file_path_by_type(self, type='CSV'):
        """
        Send the type str (a lambda input for the button connected function) to the actual function that calls the dialog window.
        
        Args:
        self
        type (str) = how to handle the operation per pre selected type
        
        """
        self.get_file_path(self.window.centralWidget(),type, pointed_path='E:/GUAPO') #match/case handling in the called method

    #data reading scripts
    def get_file_path(self,parent_window, type='CSV', pointed_path=''):
        """
        Gets file path for the selected file, according to type filter. 
        
        Args:
        self
        parent_window QMainWindow => which window to keep in front to make the dialog modal (blocking)
        type (str) = how to handle the operation per pre selected type
        pointed_path(str) = a previously used file path
        
        Returns:
        str: the file path, empty for cancelled operation
        str: the file filter used
        """
        try:
            match type:
                case 'CSV':
                    d_caption = "Select Tabulated Data"
                    d_filter = "CSV Files (*.csv);;TSV Files (*.tsv);;Text Files (*.txt);;All Files (*)"
                case 'JSON':
                    d_caption = "Select JSON Data"
                    d_filter = "JSON Files (*.json);;All Files (*)"
                case 'SQLite':
                    d_caption = "Select SQLite database to connect"
                    d_filter = "SQL database (*.db);;All Files (*)"
                case 'geographic':
                    d_caption = "Select KML/KMZ file"
                    d_filter = "KML,KMZ Files (*.kml *.kmz);;All Files (*)"
                case 'XLS':
                    d_caption = "Select Excel file"
                    d_filter = "XLS,XLSX Files (*.xls *.xlsx);;All Files (*)"
                case _:
                    raise ValueError
        except ValueError:
            self.window.update_statusbar('[ERROR] File "main.py", Function "get_file_path", Bad [file type] string.')
        except:
            self.window.update_statusbar('[ERROR] File "main.py", Function "get_file_path", Unknown error on [file type] check.')

        if not (self.active_directory and os.path.isdir(self.active_directory)): #if pre-existing path does not exists or isn't valid
            self.active_directory=''

        try:     
            self.block_execution = True
            file_path, filter_option = QFileDialog.getOpenFileName(parent_window, caption=d_caption, directory=self.active_directory, filter=d_filter)
            if (file_path and os.path.isfile(file_path)): #if returned path exists and is valid
                self.active_directory = os.path.dirname(file_path)
                self.process_read_data(file_path, type)
            else:
                raise FileNotFoundError
        except ValueError:
            self.window.update_statusbar('[ERROR] File "main.py", Function "get_file_path", Unknown error on [file type] check.')
        except FileNotFoundError:
            self.window.update_statusbar('[ERROR] File "main.py", Function "get_file_path", Bad path string or missing file.')
        except Exception as e:
            self.block_execution = False
            self.window.update_statusbar(f'[ERROR] File "main.py", Function "get_file_path", Unknown error when getting file path.\n{e}')
            print(f'{e}')


    def process_read_data(self, file_path: str='', type: str=''):
        try:
            match type:
                case 'CSV':
                    data, dataset_type, delimiter, has_header, error = self.open_CSV(file_path)
                    if not (error):
                        self.datasets.append(TableFormat(DataMode.TABLE, dtype=dataset_type,dformat=[], dheaders=data.columns.to_list(),data=data))
                        self.current_dataset_index = len(self.datasets)-1
                        self.window.set_headers(data.columns.to_list())
                        self.window.set_data_table(self.datasets[self.current_dataset_index].data.values.tolist())
                        self.window.add_dataset_item_entry('New Data', len(self.datasets)-1, data.columns.tolist(), dataset_type)
                        
                    self.block_execution = False
                case 'JSON':
                    pass
                case 'SQLite':
                    pass
                case 'geographic':
                    pass
                case 'XLS':
                    pass
                case _:
                    raise ValueError
        except ValueError:
            self.block_execution = False
            self.window.update_statusbar('[ERROR] File "main.py", Function "get_file_path", Unknown error on [file type] check.')
        except FileNotFoundError:
            self.block_execution = False
            self.window.update_statusbar('[ERROR] File "main.py", Function "get_file_path", Bad path string or missing file.')
        except Exception as e:
            self.block_execution = False
            self.window.update_statusbar(f'[ERROR] File "main.py", Function "get_file_path", Unknown error when getting file path.\n{e}')
            print(f'{e}')

    
    
    def return_col_type(self,data_item=-1, col=-1) -> DataType:
        """
        Gets the Data Type of selected column (ex: clicked)
        Args
        [int] = the selected data set item (out of all imported)
        [int] = the selected column of the data set
        Return
        [DataType] = the data type of selected column
        """           
        return self.datasets[data_item].dtype[col]


    #data wrangling scripts


    #data writing scripts


    #data visualization scripts
    

    # === Connect main methods to GUI buttons ===
    def connect_all_functions(self): #!!!!!!!!!!REMOVE THIS AND ADD THE FUNCTIONS DIRECTLY TO THE REFERENCE TO MAIN INSIDE GUI.PY
        """
        Connect main methods to GUI actions (ex: clicked)
        """        
        self.window.b_str_whitespaces.clicked.connect(self.baction_str_whitespace)
        self.window.b_str_capitalize.clicked.connect(self.baction_str_capitalization)
        self.window.b_str_blocked.clicked.connect(self.baction_str_blocked_words)
        self.window.b_str_dictionary.clicked.connect(self.baction_str_dictionary_words)  

        self.window.b_DS_open_tabulated.clicked.connect(lambda: self.get_file_path_by_type('CSV'))

    def update_dataframe_column(self, dataset_index = -1, data_frame_col = -1, new_type = DataType.TEXT, new_format = '') -> bool:
        """
        Tries to update data frame (inside DataStructure) column to data type to requested type
        Args:
        dataset_index [int]: the index for the data set
        data_frame_col [int]: the index for the data frame column
        new_type[data_format.DataType]: the type of data to switch to (if possible)
        new_format[str]: the specific formatting for the selected data type, if any

        Output:
        bool -> was operation successful? This will update GUI data accordingly
        """  
        print(f'Dataset:[{dataset_index}], DataColumn:[{data_frame_col}], New Data Type:[{str(new_type)}]')
        return True

    def print_something(self):
        print ('SUCCESFULLY PRINTED')


if __name__ == '__main__':
    main()