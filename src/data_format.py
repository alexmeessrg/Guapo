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
import numpy as np

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

class NumericOperation(Enum):
    ADDITION = 1
    SUBTRACTION = 2
    MULTIPLICATION = 3
    DIVISION = 4
    LOG = 5
    EXPONENTIAL = 6
    POWER = 7
    ROOT = 8
    CLAMP = 9

    def __str__(self):
        return self.name    
    
    def __int__(self):
        return list(self.__class__).index(self)  # Convert to int using index



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

    # ===== METHODS TO OPERATE STRING DATA ===== #
    #Method to deal with whitespaces
    def remove_whitespace(self, c_index=0, option='') -> str: #the result string
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
    
    def remove_duplicates(self, c_index=0):
        pass

    def split_text(self, c_index=0, delimiter=''):
        pass

    

    # ===== METHODS TO OPERATE NUMERIC DATA ===== #
    def operate_int(self, c_index=0, col_data: pd.Series=[], operation: NumericOperation = NumericOperation.ADDITION, num_arg: int=1) -> Tuple [bool, str, pd.Series]:
        """
        Operates on specified INTEGER column. Can be inputed many times to generate the desired operations and them applied to underlying data frame.
        Args:
        [int]: the column index in the dataframe.
        [Pandas.Series]: actual series of values
        [NumericOperation]: the operation to realize
        num_arg: the numerical argument
        Return:
        [bool]:result of the operation
        [str]:error result
        [Pandas.Series]: the resulting values of the operation (not applied, should apply later)
        """
        try: 
            col_name = self.data.columns[c_index]

            if (self.dtype[c_index]==DataType.INTEGER and (self.data[col_name].dtype== 'int32' or self.data[col_name].dtype== 'int64')): #check for correct input types
                match operation:
                    case NumericOperation.ADDITION:
                        result_series = col_data + num_arg
                    case NumericOperation.SUBTRACTION:
                        result_series = col_data - num_arg
                    case NumericOperation.MULTIPLICATION:
                        result_series = col_data * num_arg
                    case NumericOperation.DIVISION:
                        result_series = col_data / num_arg
                    case NumericOperation.LOG:
                        result_series =  np.log(col_data) if num_arg==0 else np.log10(col_data)
                    case NumericOperation.EXPONENTIAL:
                        result_series =  np.exp(col_data)
                    case NumericOperation.POWER:
                        result_series =  np.power(num_arg, col_data)
                    case NumericOperation.ROOT:
                        result_series = np.roots(num_arg, col_data)
                    case _:
                        print ("Not valid operation")
                        return False, None, None
                    
                result_series = result_series.astype(int) #keep int type

                log_message = f"""<div>Numeric operation (int) in <span style="color: gray;">Col: {col_name}[{c_index}] - Operation: {str(operation)}</span></div>"""
                return True, log_message, result_series
            
            else: #wrong data type
                return False, '[ERROR] File "data_format.py", Function "operate_int", Wrong operation type', None
          
        except Exception as e:
            error_message = f'[ERROR] File "data_format.py", Function "operate_int"\n{e}'
            return False, error_message, None
            
    def operate_float(self, c_index=0, col_data: pd.Series=[], operation: NumericOperation = NumericOperation.ADDITION, num_arg: float=1.0) -> Tuple [bool, str, pd.Series]:
        """
        Operates on specified INTEGER column. Can be inputed many times to generate the desired operations and them applied to underlying data frame.
        Args:
        [int]: the column index in the dataframe.
        [Pandas.Series]: actual series of values
        [NumericOperation]: the operation to realize
        num_arg: the numerical argument
        Return:
        [bool]:result of the operation
        [str]:error result
        [Pandas.Series]: the resulting values of the operation (not applied, should apply later)
        """
        try: 
            col_name = self.data.columns[c_index]
            if (self.dtype[c_index]==DataType.FLOAT and (self.data[col_name].dtype== 'float32' or self.data[col_name].dtype== 'float64')): #check for correct input types
                match operation:
                    case NumericOperation.ADDITION:
                        result_series = col_data + num_arg
                    case NumericOperation.SUBTRACTION:
                        result_series = col_data - num_arg
                    case NumericOperation.MULTIPLICATION:
                        result_series = col_data * num_arg
                    case NumericOperation.DIVISION:
                        result_series = col_data / num_arg
                    case NumericOperation.LOG:
                        result_series =  np.log(col_data) if num_arg==0 else np.log10(col_data)
                    case NumericOperation.EXPONENTIAL:
                        result_series =  np.exp(col_data)
                    case NumericOperation.POWER:
                        result_series =  np.power(num_arg, col_data)
                    case NumericOperation.ROOT:
                        result_series = np.roots(num_arg, col_data)
                    case _:
                        return False, None
                    

                log_message = f"""<div>Numeric operation (float) in <span style="color: gray;">Col: {col_name}[{c_index}] - Operation: {str(operation)}</span></div>"""
                return True, log_message, result_series
            
            else: #wrong data type
                return False, '[ERROR] File "data_format.py", Function "operate_float", Wrong operation type', None
          
        except Exception as e:
            error_message = f'[ERROR] File "data_format.py", Function "operate_float"\n{e}'
            return False, error_message, None    


    def clamp_int(self, col_data: pd.Series=[], low_range: int=0, high_range: int=10) -> pd.Series:
        """
        Clamps integer data in range
        """    
        return col_data.clip(lower=low_range, upper=high_range).astype(int)
    
    def clamp_float(self, col_data: pd.Series=[], low_range: float=0, high_range: float=10) -> pd.Series:
        """
        Clamps integer data in range
        """    
        return col_data.clip(lower=low_range, upper=high_range).astype(float)

    
    
    # ===== METHODS TO SEARCH DATA ===== #
    # Method to get search results
    def search_result(self, c_index=0, search_string='') -> Tuple [list, str]: #the table filter index, the result string (None if OK)
        if (self.dtype[c_index]==DataType.TEXT): #if column is a string column
            c_name = self.data.columns[c_index] #name of the column 
            hits = self.data[c_name].str.contains(search_string, case=False)
            found_indices = hits.index[hits].to_list()
            print(found_indices)
            return found_indices, None #no errors
        return None, 'Error: not a text column.'