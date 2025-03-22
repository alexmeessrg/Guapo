"""
File: main.py
Author: Alex Mees
Date: 2025-03-13
Description: Entry point for Project Guapo.
License: MIT
"""



# Standard library imports

# Third-party imports
import pandas as pd

# Local application imports
from src.fetcher import *
from src.wrangler import *
from src.gui import *
from src.data_format import *


def open_SQLite():
        Fetcher.read_SQLite("E:/GUAPO/guapo/sample/sampleSQL.db") #TODO: replace with proper file path

def open_CSV() -> Tuple [pd.DataFrame,str,str]:
    raw_data, error = Fetcher.read_CSV("E:/GUAPO/guapo/sample/sampleCSVdata.txt")
    if not (error):
        data, delimiter, has_header, error = Wrangler.handle_tabulated(raw_data) #this take the raw text data and process it        
        return data, delimiter, has_header, error
    else:
        print(error)
        return None, None, None, error




class main:
    def __init__(self):
    # === WINDOW INITIALIZATION ===
        self.app = QApplication(sys.argv) #initializes the application with command line support
        self.window = MainWindow() 
        self.window.show()

        #Global Setup
        self.use_custom_blocked_list = False #which blocked word list to use
        self.use_custom_dictionary = False
        self.custom_dictionaries = [[''],['']]
        self.active_custom_dictionary = ['']
        
        #Pre-GUI test
        print("xxxxxxx Doing tests here xxxxxxxx")
    
        data, delimiter, has_header, error = open_CSV()
    
        if not (error):
            #for testing TODO:remove
            self.thisdata = TableFormat(DataMode.TABLE, dtype=[DataType.TEXT,DataType.INTEGER,DataType.INTEGER,DataType.TEXT],dformat=[], dheaders=data.columns.to_list(),data=data)

            self.connect_all_functions()


            self.thisdata.search_result(0,'S')
            self.window.set_headers(['Country','Area','Population','Capital'])
            self.window.set_data_table(self.thisdata.data.values.tolist())
        else:
            print(error)
    
        sys.exit(self.app.exec()) #putting this here so it won't block the rest of the commands.

    #open_SQLite()
    
    # ==== GUI initialization scripts ====
    # === Actions for GUI buttons ===
    # == Method for removing whitespace
    def baction_str_whitespace(self):
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
            
            self.thisdata.capitalization_rule(col_index, option)
            self.window.set_data_table(self.thisdata.data.values.tolist())
            self.window.add_to_log([self.thisdata.data.columns[col_index], col_index, option],'str_capitalization')
            self.window.update_statusbar('Whitespace removal Operation')
                    
        except IndexError:
            self.window.update_statusbar('[ERROR] File "main.py", Function "baction_str_whitespace", Wrong data column index.')
        except ValueError:
            self.window.update_statusbar('[ERROR] File "main.py", Function "baction_str_whitespace", Wrong method option.')
        except:
            self.window.update_statusbar('[ERROR] File "main.py", Function "baction_str_whitespace", Unknown error.')


        if not (self.window.dataset_column_index < 0):
            self.thisdata.remove_whitespace(self.window.dataset_column_index,'doubles')
            self.window.set_data_table(self.thisdata.data.values.tolist())
            print(self.thisdata.data.iloc[:,self.window.dataset_column_index].to_list())
    
    # == Method for capitalization rule
    def baction_str_capitalization(self):
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
            
            self.thisdata.capitalization_rule(col_index, option)
            self.window.set_data_table(self.thisdata.data.values.tolist())
            self.window.add_to_log([self.thisdata.data.columns[col_index], col_index, option],'str_capitalization')
            self.window.update_statusbar('Capitalization Operation')
                    
        except IndexError:
            self.window.update_statusbar('[ERROR] File "main.py", Function "baction_str_capitalization", Wrong data column index.')
        except ValueError:
            self.window.update_statusbar('[ERROR] File "main.py", Function "baction_str_capitalization", Wrong method option.')
        except:
            self.window.update_statusbar('[ERROR] File "main.py", Function "baction_str_capitalization", Unknown error.')

    # == Method for blocked words rule
    def baction_str_blocked_words(self):
        try:
            col_index = self.window.dataset_column_index
            if (self.use_custom_blocked_list):
                #implement this later
                blocked_words_list = ''
                pass
            else:
                blocked_words_list = constants.BLOCKED_WORD_LIST #user should be able to review these TODO:add option to add own list
            
            self.thisdata.blocked_words(col_index, blocked_words_list)
            self.window.set_data_table(self.thisdata.data.values.tolist())
            self.window.add_to_log([self.thisdata.data.columns[col_index], col_index, self.use_custom_blocked_list],'str_blocked')
            self.window.update_statusbar('Blocked word Operation')
                    
        except IndexError:
            self.window.update_statusbar('[ERROR] File "main.py", Function "baction_str_blocked_word", Wrong data column index.')
        except ValueError:
            self.window.update_statusbar('[ERROR] File "main.py", Function "baction_str_blocked_word", Wrong method option.')
        except:
            self.window.update_statusbar('[ERROR] File "main.py", Function "baction_str_blocked_word", Unknown error.')

    # == Method for dictionary words replacement
    def baction_str_dictionary_words(self):
        try:
            col_index = self.window.dataset_column_index
            if (self.use_custom_dictionary):
                #implement this later
                dictionary = self.active_custom_dictionary
                pass
            else:
                dictionary = constants.COMMON_DICTIONARY_REPLACEMENTS
            
            self.thisdata.dictionary_words(col_index, dictionary)
            self.window.set_data_table(self.thisdata.data.values.tolist())
            self.window.add_to_log([self.thisdata.data.columns[col_index], col_index, self.use_custom_dictionary],'str_dictionary')
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
        self.get_file_path(self.window.centralWidget(),type, pointed_path='E:/GUAPO')

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

        if not (pointed_path and os.path.isdir(pointed_path)): #if pre-existing path exists and is valid
            pointed_path=''    

        try:     
            file_path, filter_option = QFileDialog.getOpenFileName(parent_window, caption=d_caption, directory=pointed_path, filter=d_filter)
        except:
            self.window.update_statusbar('[ERROR] File "main.py", Function "get_file_path", Unknown error when getting file path.')
        finally:
            if (file_path and os.path.isdir(file_path)): #if pre-existing path exists and is valid
             
            #FROM HERE ON, START TO PROCESS THE DATA.
            #########
            ####################
            ################

    

    #data wrangling scripts


    #data writing scripts


    #data visualization scripts
    

    # === Connect main methods to GUI buttons ===
    def connect_all_functions(self):
        self.window.b_str_whitespaces.clicked.connect(self.baction_str_whitespace)
        self.window.b_str_capitalize.clicked.connect(self.baction_str_capitalization)
        self.window.b_str_blocked.clicked.connect(self.baction_str_blocked_words)
        self.window.b_str_dictionary.clicked.connect(self.baction_str_dictionary_words)  

        self.window.b_DS_open_tabulated.clicked.connect(lambda: self.get_file_path_by_type('CSV'))

    def printsomething():
        print('Button Clicked')





if __name__ == '__main__':
    main()