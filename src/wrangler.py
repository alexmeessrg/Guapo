"""
File: wrangler.py
Author: Alex Mees
Date: 2025-03-13
Description: Scripts for understanding, cleaning and consolidating data
License: MIT
"""
# Standard library imports
import math
from typing import Tuple


# Third-party imports
import pandas as pd

# Local application imports
from . import constants
from .data_format import DataType


    

class Wrangler:
    @staticmethod
    def header_comprehension(header, sample_data, delimiter) -> Tuple [list, str, str]: #the headers, the string for the delimiter, possible errors
        
        if not delimiter==None: #if user tells the delimiter to use, use it. If not, try to guess it.
            header_list = header.split(delimiter)
            return header_list, delimiter, None

        else: #do pattern matching to understand what is the delimiter.
            common_delimiters =  constants.COMMON_DELIMITERS
            sample_delimiter_count = [] #counting number of occurences for delimiters
            
            for delimiter in common_delimiters: #iterate delimiter and try to find the number of them
                del_count = 0
                for line in sample_data:
                    del_count =+ line.count(delimiter)
                sample_delimiter_count.append(del_count)
            
            max_finds = max(sample_delimiter_count) #the maximum number of delimiter occurences
            top_candidates = [index for index, num in enumerate(sample_delimiter_count) if num == max_finds] #find all possible index of possible delimiters from list of maximum delimiters

            if len(top_candidates)==1: #if I only have 1 candidate for top delimiter, use that. If not, iterate through all columns and decide if split size is consistent.
                found_delimiter = common_delimiters[top_candidates[0]]
                header_list = header.split(found_delimiter)
                return header_list, found_delimiter, None
            else:
                split_size = []
                for candidate in top_candidates: #for each delimiter candidate, check column consistency
                    delim = common_delimiters[candidate]
                    col_count = 0
                    for line in sample_data:
                        if (sample_data[0].split(delim) != line.split(delim)):
                            top_candidates.remove(candidate) #if any line split is different that first line split, remove from candidates
               
                if len(top_candidates)!=0: #if I only have 1 candidate for top delimiter, use that. If more than 1 found use first found (likely comma)
                    found_delimiter = common_delimiters[top_candidates[0]]
                    header_list = header.split(found_delimiter)
                    return header_list, found_delimiter, None
                else: #no proper delimiter found, using single column until user define a delimiter
                    return header,'',None
    
    @staticmethod
    def break_tabulated(raw_data,delimiter,has_header=True,header=[]) -> Tuple [pd.DataFrame, list[DataType], str, bool, str]: #the converted data frame, the delimiter, has_header, possible errors
        col_count = len(raw_data[0].split(delimiter)) #there could be a mistake in the header/first line making this number unreliable

        if (has_header):
            raw_data = raw_data[1:] #exclude first line if it has a header
        else:
            header = list(range(1, col_count)) #create numeric headers if none available, doesn't have to exclude first line
        
        data = []
        for line in raw_data:
            data.append(line.split(delimiter)) #split values into lists

        df = pd.DataFrame(data, columns=header) #create a Panda Data Frame with the data and the created headers

        data_types = [DataType.TEXT] * col_count #initialize a list with all data types da TEXT

        sample_size = min (constants.DATA_TYPE_SAMPLE_SIZE, df.size-1) #the amount of data to sample clamped by data lenght if shorter than
        total_int_positives = 0
        total_float_positives = 0

        #Should try to autodetect integers, floats, dates => other should be opt-in at this moment.

        for index, (col_name, col_data) in enumerate(df.items()):           

            total_int_positives, total_float_positives = Wrangler.check_type_number(col_data.tolist(), sample_size)

            if (total_int_positives/sample_size > 0.5) or (total_float_positives/sample_size > 0.5):
                if (total_int_positives > total_float_positives):
                    df[col_name] = df[col_name].astype('int64') #change data type of current column to int64
                    data_types[index] = DataType.INTEGER
                else:
                    df[col_name] = df[col_name].astype('float64') #change data type of current column to int64
                    data_types[index] = DataType.FLOAT
        
        #print (df.dtypes)
        return df, data_types, delimiter, has_header, None



    @staticmethod
    def check_type_number(data_list,sample_size) -> Tuple [int, int]: #give a grade for the likelyhood of it being a number column
        data_size = len(data_list)
        sample_list = data_list[0:min(sample_size,data_size-1)] #get sample data from first "sample_size" items.
        total_int_positives = 0
        total_float_positives = 0
        
        for item in sample_list:
            try:
                int(item)
                total_int_positives += 1
            except ValueError:
                try:
                    float(item)
                    total_float_positives += 1
                except ValueError:
                    pass
        return total_int_positives, total_float_positives






    @staticmethod
    def handle_tabulated(raw_data,delimiter=None,has_header=True) -> Tuple [pd.DataFrame, list[DataType], str, bool, str]: #the actual array, delimiter used, possible errors

        #THERE NEEDS TO BE A METHOD TO IDENTIFY HEADER TYPES.

        if (has_header):
            if (len(raw_data)<2): #if you exclude the header there is no data.
                return None, '', True, "Data doesn't have enough lines when excluding headers"
            else:
                header = raw_data[0]
                sample_data = raw_data[0:min(4,len(raw_data)-1)] #tries to sample 4 lines or less if data is small
                header, delimiter, error = Wrangler.header_comprehension(header, sample_data, delimiter)
                data, data_types, delimiter, has_header, error = Wrangler.break_tabulated(raw_data,delimiter,has_header,header)
                return data, data_types, delimiter, has_header, error
            




