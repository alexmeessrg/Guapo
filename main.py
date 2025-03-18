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

#Actions for the Buttons    
def baction_str_whitespace(datastructure=TableFormat(), index=-1, option='trailing'):
    if not (index<0):
        datastructure.remove_whitespace(index, option)

def baction_str_capitalization(datastructure=TableFormat(), index=-1, option='all'):
    if not (index<0):
        datastructure.capitalization_rule(index, option)


def printsomething():
     print('Button Clicked')


def main():
    #Initialization 
    app = QApplication(sys.argv) #initializes the application with command line support
    window = MainWindow()
    window.show()

    #add event handler to all buttons in the main window   
    window.set_event_handlers('b_str_blocked',printsomething)
    #Pre-GUI test
    print("xxxxxxx Doing tests here xxxxxxxx")
    
    data, delimiter, has_header, error = open_CSV()
    if not (error):
        #print (header)
        thisdata = TableFormat(DataMode.TABLE, dtype=[DataType.TEXT,DataType.INTEGER,DataType.INTEGER,DataType.TEXT],dformat=[], dheaders=data.columns.to_list(),data=data)
        baction_str_whitespace(thisdata, 0, 'doubles')
        baction_str_capitalization(thisdata, 0, 'all')
        thisdata.search_result(0,'S')
        window.set_headers(['Country','Area','Population','Capital'])
        #print(data)
        print("Start setting table")
        window.set_data_table(thisdata.data.values.tolist())
        print("End setting table")
    else:
        print(error)
    

    #open_SQLite()
    
    #GUI initialization scripts
    
    #data reading scripts
    

    #data wrangling scripts


    #data writing scripts


    #data visualization scripts
    

    sys.exit(app.exec()) #putting this here so it won't block the rest of the commands.




if __name__ == '__main__':
    main()