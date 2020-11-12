#
# Library Imports
#

import sqlite3


#
# Function Definitions
#

def get_sqlite_database_path():
    import os

    sqlite_database_path = os.getcwd() + '/' + 'thingiverse.db'

    return sqlite_database_path
    

def get_database_connection(sqlite_database_path):
    # Create database connection to local SQLite3 DB
    import sqlite3

    database_connection = sqlite3.connect(sqlite_database_path)

    return database_connection


def get_database_cursor(database_connection):
    # Initialize cursor to SQLite3 DB
    database_cursor = database_connection.cursor()

    return database_cursor


def close_database_cursor(database_cursor):
    # Close SQLite3 DB cursor
    database_cursor.close()


def close_database_connection(database_connection):
    # Close SQLite3 DB connection
    database_connection.close()


def create_thingiverse_table(database_connection, database_cursor, table_name):
    # Create database table 'thingiverse_catalog'
    sql = f'''CREATE TABLE {table_name} (
                                                id integer PRIMARY KEY,
                                                page_number integer,
                                                page_title text,
                                                datestamp text
                                               )'''

    database_cursor.execute(sql)
    database_connection.commit()


def insert_dummy_record_into_thingiverse_table(database_connection, database_cursor, table_name):
    # Add a dummy record with page number 0 to act as a starting point for thingiverse_scraper.py
    record_id = None
    page_number = 0
    page_title = 'dummy_record'
    datestamp = None

    sql = f'''INSERT INTO {table_name} (id, page_number, page_title, datestamp) VALUES (?, ?, ?, ?)'''

    database_cursor.execute(sql, (record_id, page_number, page_title, datestamp))

    database_connection.commit()


#
# Configuration Information
#

table_name = 'thingiverse_catalog'


#
# Start Here
#

sqlite_database_path = get_sqlite_database_path()
database_connection = get_database_connection(sqlite_database_path)
database_cursor = get_database_cursor(database_connection)

create_thingiverse_table(database_connection, database_cursor, table_name)
insert_dummy_record_into_thingiverse_table(database_connection, database_cursor, table_name)

close_database_cursor(database_cursor)
close_database_connection(database_connection)