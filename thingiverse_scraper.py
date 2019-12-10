# Libraries
import time
import requests
import mysql.connector

# Runtime variables
http_success = 200
html_title_limit = 150
worker_start_range = None
worker_end_range = 5000000
empty_html_title = 'Empty_Page'
download_directory = '/root/thingiverse_scrape/files/'
sleep_timer_seconds = 4
remote_zip_buffer_size = 100000000 #Size in bytes

# Function definitions
def create_database_connection():
    db_connection = mysql.connector.connect(user='database_user', password='SuperSecretPassword', database='thingiverse')
    db_cursor = db_connection.cursor()
    return db_connection, db_cursor

def retrieve_database_result(db_connection, db_cursor, query):
    # Only useful for single value retrievals otherwise it'll take the last value of tuple
    # Find better way to do this / Current workaround is using "...LIMIT 1"
    db_cursor.execute(query)
    for i in db_cursor:
        item = i
    return item

def submit_database_result(query):
    db_connection, db_cursor = create_database_connection()
    db_cursor.execute(query)
    db_connection.commit()
    close_database_connection(db_connection, db_cursor)

def close_database_connection(db_connection, db_cursor):
    db_cursor.close()
    db_connection.close()

def retrieve_index():
    db_connection, db_cursor = create_database_connection()
    result = retrieve_database_result(db_connection, db_cursor, "SELECT page_num FROM thingiverse_catalog ORDER BY id DESC LIMIT 1")
    result = int(result[0])
    close_database_connection(db_connection, db_cursor)
    return result

def request_page(page_id):
    url = 'https://www.thingiverse.com/thing:' + str(page_id)
    time.sleep(sleep_timer_seconds)
    response = requests.get(url)
    return url, response

def check_download_directory():
    import os
    if not os.path.exists(download_directory):
        try:
            os.makedirs(download_directory)
        except OSError:
            import sys
            print('Download directory does not exist or is not valid. Exiting...')
            sys.exit()

def download_zip(current_page, url, html_title):
    # Pause for n seconds to avoid hammering Thingiverse
    time.sleep(sleep_timer_seconds)
    local_filepath = f'{download_directory}{current_page}-{html_title}.zip'
    chunk_interations = 0
    with requests.get(url, stream=True) as remote_zip_file:
        remote_zip.raise_for_status()
        with open(local_filepath, 'wb') as local_zip_file:
            for chunk in remote_zip.iter_content(chunk_size=remote_zip_buffer_size):
                chunk_iterations += 1
                local_zip_file.write(chunk)
    result = (
              f'{download_link}' + '\n' \
              f'Downloaded in: {chunk_iterations} chunks' + '\n'
             )
    return result

# Start Here
if not worker_start_range:
    worker_start_range = retrieve_index() + 1

check_download_directory()

for current_page in range(worker_start_range, worker_end_range):
    url, response = request_page(current_page)

    if response.status_code == http_success:
        html_title_start = response.text.find('<title>') + len('<title>')
        html_title_end = response.text.find('</title>')
        html_title = response.text[html_title_start:html_title_end]
        html_title = html_title.replace('/', '-')
        if len(html_title) > html_title_limit:
            html_title = html_title[0:html_title_limit]
    else:
        html_title_start = 0
        html_title_end = 0
        html_title = empty_html_title

    if empty_html_title not in html_title:
        print(download_zip(current_page, url, html_title))

    database_insert_query = f'''INSERT INTO thingiverse_catalog VALUES (NULL, {current_page}, "{html_title}", CURRENT_TIMESTAMP)'''

    submit_database_result(database_insert_query)
