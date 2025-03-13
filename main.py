"""
File: main.py
Author: Alex Mees
Date: 2025-03-13
Description: Entry point for Project Guapo.
License: MIT
"""



# Standard library imports
# Third-party imports


# Local application imports
from src.fetcher import *
from src.wrangler import *




def main():
    #Initialization 
    

    #Pre-GUI test
    print("xxxxxxx Doing tests here xxxxxxxx")
    raw_data, error = Fetcher.read_CSV("E:/GUAPO/guapo/sample/sampleCSVdata.txt")
    if not (error):
        header, delimiter, error = Wrangler.handle_tabulated(raw_data)
        if not (error):
            print (header)
        else:
            print(error)
    else:
        print(error)
  
    #GUI initialization scripts
    
    #data reading scripts
    

    #data wrangling scripts


    #data writing scripts


    #data visualization scripts

    pass



if __name__ == '__main__':
    main()