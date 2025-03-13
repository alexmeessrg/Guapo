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

# Local application imports
from . import constants


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
    def handle_tabulated(raw_data,delimiter=None,has_header=True) -> Tuple [list, str, str]: #the actual array, possible errors
        for line in raw_data:
            print(line)

        if (has_header):
            if (len(raw_data)<2): #if you exclude the header there is no data.
                return None, '', "Data doesn't have enough lines when excluding headers"
            else:
                header = raw_data[0]
                sample_data = raw_data[0:min(4,len(raw_data)-1)] #tries to sample 4 lines or less if data is small
                header, delimiter, error = Wrangler.header_comprehension(header, sample_data, delimiter)
                return header, delimiter, error



