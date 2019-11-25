# Libraries

import time
import requests
import mysql.connector

# Runtime variables
# TODO: Add config file to capture runtime variables

http_success = 200
html_title_limit = 150
worker_start_range = ''
worker_end_range = 5000000
empty_html_title = 'empty_page'
download_directory = '/root/thingiverse_scrape/files/'

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
    result = retrieve_database_result(db_connection, db_cursor, "SELECT page_num FROM catalog ORDER BY id DESC LIMIT 1")
    result = int(result[0])
    close_database_connection(db_connection, db_cursor)
    return result

def request_page(page_id):
    url = 'https://www.thingiverse.com/thing:' + str(page_id)
    take_a_nap()
    response = requests.get(url)
    return url, response

def take_a_nap():
    # take_a_nap() is a crude mechanism used to throttle requests to ad-hoc adhere to robots.txt guidelines
    time.sleep(4)

def check_download_directory():
    import os
    if not os.path.isdir(download_directory):
        # TODO: Add prompt to create directory that doesn't exist
        import sys
        print('Download directory does not exist or is not valid. Exiting...')
        sys.exit()

def download_zip(current_page, url, html_title):
    zip_response = requests.get(url + '/zip')
    take_a_nap()
    print('Downloading zip file for ' + url + '  ' + html_title)
    filepath = download_directory + '{}-{}.zip'.format(str(current_page), html_title)
    # TODO: Add buffer friendly download option if possible / Exceptionally large files fail on download
    with open(filepath, 'wb') as zip_file:
        zip_file.write(zip_response.content)

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
    print('{} {} {} {}'.format(url, html_title_start, html_title_end, html_title))
    if empty_html_title not in html_title:
        download_zip(current_page, url, html_title)
    query = '''INSERT INTO catalog VALUE(NULL, {}, "{}", CURRENT_TIMESTAMP, 0)'''.format(current_page, html_title)
    submit_database_result(query)
