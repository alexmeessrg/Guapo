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
import sqlite3
import csv
from typing import Tuple

# Third-party imports
import pandas as pd

# Local application imports


class Fetcher:

    @staticmethod
    def read_CSV(file_path) -> Tuple[list, str]: #to read from tabulated files
        try:
            with open(file_path, "r", encoding="utf-8") as file: #this also auto-close file after reading.
                content = [line for line in file.readlines()]
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
    
    @staticmethod
    def read_SQLite(file_path) -> Tuple[pd.DataFrame, list, str]: #output the dataframe, headers, errors
        conn = sqlite3.connect(file_path) #connect to database
        #conn = sqlite3.connect("':memory") create database in memory
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users2 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            email TEXT UNIQUE
        )
        """)
        conn.commit()
        table_name = "users2"
        cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name=?", (table_name,))
        exists = cursor.fetchone()

        if not (exists):
            cursor.execute("INSERT INTO users2 (name, age, email) VALUES (?, ?, ?)", 
               ("Alice", 25, "alice@example.com"))
            cursor.execute("INSERT INTO users2 (name, age, email) VALUES (?, ?, ?)", 
               ("John", 32, "john@example.com"))        
            cursor.execute("INSERT INTO users2 (name, age, email) VALUES (?, ?, ?)", 
               ("Peter", 50, "peter@example.com"))
            conn.commit()  # Save changes

        df = pd.read_sql_query("SELECT * FROM users", conn) #table to data frame

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        print("Tables in database")
        for table in tables:
            print(table)   


        conn.close()
        print(df)
        print(df.dtypes)
        df_types = df.applymap(type)
        print(df_types)
        


