# Thingiverse Web Scraper
#
# Scans a pre-determined range of 'things' from thingiverse and downloads both the zip
# file containing .stl and design files as well as the page source for the 'thing.' This
# allows for additional parsing to scrape tags, names and other details about a thing.

#
# Library Imports
#
import time
import datetime
import sqlite3

#
# Configuration Data
#
http_success_status_codes = [200]
thing_start_range = None
thing_end_range = 5000000

page_title_max_size = 150

# Same table name as defined in setup_thingiverse_database.py
thingiverse_table_name = 'thingiverse_catalog'

# Ideally, keep this above 3 to not hammer Thingiverse with requests
delay_between_downloads_seconds = 4

# Buffer (chunk) size when downloading / Files will be downloaded 100MB at a time
remote_zip_buffer_size = 102400000

#
# Function Definitions
#
def get_download_file_paths():
    # Check if both download directories (files and html) exist
    # and create if they do not
    import os

    current_directory = os.getcwd() + '/'

    files_directory = current_directory + 'files' + '/'
    html_directory = current_directory + 'html' + '/'

    if not os.path.exists(files_directory) and not os.path.exists(html_directory):
        try:
            os.makedirs(files_directory)
            os.makedirs(html_directory)
        except OSError:
            import sys
            print('File or HTML directory cannot be created... Exiting')
            sys.exit()

    return files_directory, html_directory


def get_sqlite_database_path():
    # Get local SQLite3 DB path
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


def get_last_page_number(database_connection, database_cursor, table_name):
    sql = f'''SELECT page_number FROM {table_name} ORDER BY page_number DESC LIMIT 1'''

    database_cursor.execute(sql)

    try:
        page_number = database_cursor.fetchone()[0]
    except TypeError:
        page_number = None

    return page_number


def insert_record_into_thingiverse_table(database_connection, database_cursor, table_name, table_record_id, page_number, page_title, timestamp):
    sql = f'''INSERT INTO {table_name} (id, page_number, page_title, datestamp) VALUES (?, ?, ?, ?)'''

    database_cursor.execute(sql, (table_record_id, page_number, page_title, timestamp))

    database_connection.commit()


def check_if_valid_thingiverse_page_and_retrieve_html_and_page_title(thing_id, thingiverse_url, http_success_status_codes):
    # Though this function may seem clunky, 'check if valid' and 'retrieve html' 
    # are combined to reduce the number of requests sent to Thingiverse per thing. 
    import requests

    response = requests.get(thingiverse_url + str(thing_id))

    thingiverse_thing_html = None
    thingiverse_thing_page_title = None

    if response.status_code in http_success_status_codes:
        thingiverse_thing_html = response.text

        # Beautiful soup could be used for this but for something this simple, an import seems
        # unnecessary
        html_title_start = thingiverse_thing_html.find('<title>') + len('<title>')
        html_title_end = thingiverse_thing_html.find('</title>')

        thingiverse_thing_page_title = thingiverse_thing_html[html_title_start:html_title_end]

        # Remove forward slashes as files will include page title and forward slashes make
        # file names look like directories
        thingiverse_thing_page_title = thingiverse_thing_page_title.replace('/', '-')

    return thingiverse_thing_html, thingiverse_thing_page_title


def download_thingiverse_zip_file(files_directory, thing_id, thing_page_title, thingiverse_url, http_success_status_codes, remote_zip_buffer_size):
    import requests

    local_zip_file_path = files_directory + f'{thing_id}-{thing_page_title}.zip'
    thingiverse_zip_file_url = thingiverse_url + f'{thing_id}/zip'

    with requests.get(thingiverse_zip_file_url, stream=True) as f_remote_thingiverse_zip:
        if f_remote_thingiverse_zip.status_code in http_success_status_codes:
            with open(local_zip_file_path, 'wb') as f_local_thingiverse_zip:
                for chunk in f_remote_thingiverse_zip.iter_content(chunk_size=remote_zip_buffer_size):
                    f_local_thingiverse_zip.write(chunk)

    print(f'Thing ID: {thing_id} downloaded...')

#
# Start Here
#
files_directory, html_directory = get_download_file_paths()

sqlite_database_path = get_sqlite_database_path()
database_connection = get_database_connection(sqlite_database_path)
database_cursor = get_database_cursor(database_connection)

thingiverse_url = 'https://www.thingiverse.com/thing:'

if not thing_start_range:
    thing_start_range = get_last_page_number(database_connection, database_cursor, thingiverse_table_name)

    if thing_start_range:
        thing_start_range += 1
    else:
        thing_start_range = 1

for current_page in range(thing_start_range, thing_end_range):
    thing_id = current_page
    thing_timestamp = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

    thing_html, thing_page_title = check_if_valid_thingiverse_page_and_retrieve_html_and_page_title(thing_id, thingiverse_url, http_success_status_codes)
    if not thing_html and not thing_page_title:
        # Write empty page details to database and continue
        insert_record_into_thingiverse_table(database_connection, database_cursor, thingiverse_table_name, None, thing_id, 'Blank Page', thing_timestamp)
        continue

    if len(thing_page_title) > page_title_max_size:
        thing_page_title = thing_page_title[:page_title_max_size]

    # If thing URL is valid, write page HTML to ../html/ directory
    with open(html_directory + f'{thing_id}-{thing_page_title}.txt', 'w') as f_html_file:
        f_html_file.write(thing_html)

    # Download Thing zip file
    download_thingiverse_zip_file(files_directory, thing_id, thing_page_title, thingiverse_url, http_success_status_codes, remote_zip_buffer_size)
    insert_record_into_thingiverse_table(database_connection, database_cursor, thingiverse_table_name, None, thing_id, thing_page_title, thing_timestamp)

    time.sleep(delay_between_downloads_seconds)

close_database_cursor(database_cursor)
close_database_connection(database_connection)