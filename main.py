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




def main():
    # === WINDOW INITIALIZATION ===
    app = QApplication(sys.argv) #initializes the application with command line support
    window = MainWindow()
    window.show()

    # === ACTIONS FOR GUI BUTTONS ===    
    def baction_str_whitespace():
        print("Remove Whitespace")
        if not (window.dataset_column_index < 0):
            thisdata.remove_whitespace(window.dataset_column_index,'doubles')
            window.set_data_table(thisdata.data.values.tolist())
            print(thisdata.data.iloc[:,window.dataset_column_index].to_list())

    def baction_str_capitalization():
        if not (window.dataset_column_index<0):
            thisdata.capitalization_rule(window.dataset_column_index, 'all')
            window.set_data_table(thisdata.data.values.tolist())

    # == CONNECT TO APPROPRIATE GUI EVENTS  
    window.b_str_whitespaces.clicked.connect(baction_str_whitespace)
    window.b_str_capitalize.clicked.connect(baction_str_capitalization)
    

    
    
    #Pre-GUI test
    print("xxxxxxx Doing tests here xxxxxxxx")
    
    data, delimiter, has_header, error = open_CSV()
    
    if not (error):
        #for testing TODO:remove
        thisdata = TableFormat(DataMode.TABLE, dtype=[DataType.TEXT,DataType.INTEGER,DataType.INTEGER,DataType.TEXT],dformat=[], dheaders=data.columns.to_list(),data=data)




        thisdata.search_result(0,'S')
        window.set_headers(['Country','Area','Population','Capital'])
        window.set_data_table(thisdata.data.values.tolist())

    else:
        print(error)
    

    #open_SQLite()
    
    #GUI initialization scripts
    
    #data reading scripts
    

    #data wrangling scripts


    #data writing scripts


    #data visualization scripts
    

    sys.exit(app.exec()) #putting this here so it won't block the rest of the commands.


    def printsomething():
        print('Button Clicked')





if __name__ == '__main__':
    main()