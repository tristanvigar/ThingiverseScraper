import requests
import os

#
# Configuration Data
#

# Set download link to thingverse URL with zip link. Example: https://www.thingiverse.com/thing:1376314/zip
download_link = 'https://www.thingiverse.com/thing:1376314/zip'

# Set local directory to save file to
local_directory = ''

#
local_file_name = '' or 'thingiverse_file.zip'

# Set custom buffer size
buffer_size = 100000000


#
# Start Here
#

if not download_link:
    import sys

    print('download_link is not defined')
    sys.exit()

if not local_directory:
    local_directory = os.getcwd()

with requests.get(download_link, stream=True) as remote_file:
    remote_file.raise_for_status()
    with open(local_directory + '/' + local_file_name, 'wb') as local_file:
        chunk_iters = 0
        for chunk in remote_file.iter_content(chunk_size=buffer_size):
            if chunk:
                chunk_iters += 1
                local_file.write(chunk)

print(f'''
          Link: {download_link}
          Downloaded in: {chunk_iters} chunk(s)
          With buffer size of: {buffer_size}
      ''')
