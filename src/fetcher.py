"""
File: fetcher.py
Author: Alex Mees
Date: 2025-03-13
Description: Scripts for reading data from files
License: MIT
"""
# Standard library imports
import os
import json
import csv
from typing import Tuple

# Third-party imports


# Local application imports


class Fetcher:

    @staticmethod
    def read_CSV(file_path) -> Tuple[list, str]: #to read from tabulated files
        try:
            with open(file_path, "r", encoding="utf-8") as file: #this also auto-close file after reading.
                content = [line.strip() for line in file.readlines()] #removes \n and leading, trailing whitespaces
                if len(content)==0:
                    return None, f"Empty file: {file_path}"
                else:
                    return content, None

        except FileExistsError:
            return None, f"File path does not exist: {file_path}."
        except FileNotFoundError:
            return None, f"File not found: {file_path}."
        except Exception:
            return None, f"Reading file error: unknown error."