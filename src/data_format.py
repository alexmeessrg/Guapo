"""
File: data_format.py
Author: Alex Mees
Date: 2025-03-17
Description: Class for defining data structure
License: MIT
"""
# Standard library imports
from typing import Tuple
from enum import Enum

# Third-party imports
import pandas as pd

# Local application imports

class DataType(Enum):
    TEXT = 1 #plain text
    INTEGER = 2 #integer values
    FLOAT = 3 #float values
    DATE = 4 #data values (needs special formating info) (MM/DD/YYYY - DD/MM/YYYY - YYYY/MM/DD - DD/m/YY - XXXXXXX)
    TIME = 5 #not referenced time (not tied to date)
    GEOSPATIAL = 6 #LAT/LONG, LAT, LON, degrees, UTM -> 36.48S 43.84W
    VECTOR = 7 #vectors, position/velocity. Not necessarily tied to frame of reference
    DICTIONARY = 7 #a JSON file, XML
    BOOLEAN = 9 #TRUE/FALSE

    def __str__(self):
        return self.name
    
    def __int__(self):
        return list(self.__class__).index(self)  # Convert to int using index

    #column info example: {type=DataType.DATE, format='DD/MM/YYYY'}

class DataFormats(): #some extra especial formating for data types (used to change display and converting storage format)
    FloatFormats = ['0.0','1eN','1/1','%','Binary','Hex','Octal','Currency']
    DateFormats = ['dd/mm/yyyy', 'dd/mm/yy', 'dd/MM/yyyy', 'dd/MM/yyyy', 'mm/dd/yyyy', 'MM/dd/yyyy', 'mm/yyyy', 'MM/yyyy']
    GeoSpatialFormats = ['UTM:Zone,Lat,Long','UTM:Lat,Long', 'UTM:Lat', 'UTM:Long', 'UTM:Zone','DD:Lat,Long','DD:Lat','DD:Long', 'DMS:Lat', 'DMS:Long', 'DMS:Lat,Long','DDM:Lat','DDM:Long','DDM:Lat,Long','OpenLocationCode']

class DataMode(Enum): #how will the data be handled
    TABLE = 1 #data will be structured as a table (row x columns)
    DICTIONARY = 2 #data will be structured as a Dictionary (JSON, XML)
    SQLITE = 3 #data will be structured as a SQLite database 


class DataStructure(): #one for each data group
    def __init__(self, dmode=DataMode.TABLE, dtype: list[DataType]= None, dformat=[], dheaders=[],edits=[]):
        self.dmode = dmode #mode of data to use
        self.dtype = dtype #array with identifiers for each data column
        self.dformat = dformat #additional formating for each column data
        self.dheaders = dheaders #labels for each data item, id or key
        self.edits = edits #log of edits created on this data structure
        self.dname = '' #the data structure identifier

class TableFormat(DataStructure):
    def __init__(self, dmode=DataMode.TABLE, dtype: list[DataType]= None, dformat=[], dheaders=[],edits=[], data=pd.DataFrame()):
        super().__init__(dmode=DataMode.TABLE, dtype=dtype, dformat=dformat, dheaders=dheaders,edits=edits)
        self.data = data

    # ===== METHODS TO CLEAN STRING DATA ===== #
    #Method to deal with whitespaces
    def remove_whitespace(self, c_index=0, option='trailing') -> str: #the result string
        #options are trailing, leading, both, double space, all of the above
        if (self.dtype[c_index]==DataType.TEXT):
            c_name = self.data.columns[c_index]
            match option:
                case 'trailing':
                    self.data[c_name] = self.data[c_name].str.rstrip()
                case 'leading':
                    self.data[c_name] = self.data[c_name].str.lstrip()
                case 'both':
                    self.data[c_name] = self.data[c_name].str.strip()
                case 'doubles':
                    hits = self.data[c_name].str.findall(r'\s{2,}')
                    print(sum(len(hit) for hit in hits)) #the number of operations that it will generate
                    self.data[c_name] = self.data[c_name].str.replace(r'\s{2,}','', regex=True) #replace anything with 2 or more consecutive spaces.
                case 'all':
                    self.data[c_name] = self.data[c_name].str.strip()
                    self.data[c_name] = self.data[c_name].str.replace(r'\s{2,}','', regex=True)     
                case _:
                    return "Error: not a valid string operation."
            return None
        else:
            return "Error: not a string column."
    
    # Method to deal with capitalization    
    def capitalization_rule(self, c_index=0, option='all') -> str: #the result string
        #options are 'all' (words), 'each' (word), 'first' (word), 'lowercase', 'invert'
        if (self.dtype[c_index]==DataType.TEXT):
            c_name = self.data.columns[c_index]
            match option:
                case 'all':
                    self.data[c_name] = self.data[c_name].str.upper()
                case 'each':
                    self.data[c_name] = self.data[c_name].str.title()
                case 'first':
                    self.data[c_name] = self.data[c_name].str.capitalize()
                case 'lowercase':
                    self.data[c_name] = self.data[c_name].str.lower()
                case 'invert':
                    self.data[c_name] = self.data[c_name].str.swapcase()    
                case _:
                    return "Error: not a valid string operation."
            return None
        else:
            return "Error: not a string column."

    # Method to deal with blocked words
    def blocked_words(self, c_index=0, blockedlist=['']) -> str: #the result string
        bad_words = blockedlist
        if (self.dtype[c_index]==DataType.TEXT): #if column is a string column
            c_name = self.data.columns[c_index]
            for bad_word in bad_words:
                self.data[c_name] = self.data[c_name].str.replace(bad_word,'*' * len(bad_word), regex=True) #replace all bad words with **** with the same length as the original
            return None #no errors
        return 'Error: not a text column.'

    
    # Method to deal with dictionary words
    def dictionary_words(self, c_index=0, old_list=[''], new_list=['']) -> str: #the result string (None if OK)
        if (self.dtype[c_index]==DataType.TEXT): #if column is a string column
            c_name = self.data.columns[c_index]
            for i, old_word in old_list:
                self.data[c_name] = self.data[c_name].str.replace(old_word,new_list[i], regex=True)
            return None #no errors
        return 'Error: not a text column.'

    # Method to get string statistics
    def word_statistics(self, c_index=0) -> Tuple [set, list, str]: #the result string (None if OK)
        if (self.dtype[c_index]==DataType.TEXT): #if column is a string column
            c_name = self.data.columns[c_index] #name of the column 
            unique_words = set(self.data[c_name].values) #the unique words per column
            word_count = list() #the total per unique word
            for word in unique_words:
                hits = self.data[c_name].str.findall(word)
                word_count.append(sum(len(hit) for hit in hits))
            return unique_words, word_count, None #no errors
        return None, None, 'Error: not a text column.'  
     
    # Method to get search results
    def search_result(self, c_index=0, search_string='') -> Tuple [list, str]: #the table filter index, the result string (None if OK)
        if (self.dtype[c_index]==DataType.TEXT): #if column is a string column
            c_name = self.data.columns[c_index] #name of the column 
            hits = self.data[c_name].str.contains(search_string, case=False)
            found_indices = hits.index[hits].to_list()
            print(found_indices)
            return found_indices, None #no errors
        return None, 'Error: not a text column.'