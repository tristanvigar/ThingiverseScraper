import requests
import time

download_link = 'https://www.thingiverse.com/thing:1376314/zip'
local_file = '/home/tvigar/thingiverse_local_file.zip'
buffer_size = 100000000

with requests.get(download_link, stream=True) as remote_zip_file:
    remote_zip_file.raise_for_status()
#        for i in remote_zip_file.iter_content(chunk_size=buffer_size):
#            time.sleep(2)
#            chunk_iters += 1
    with open(local_file, 'wb') as local_zip_file:
        chunk_iters = 0
        for chunk in remote_zip_file.iter_content(chunk_size=buffer_size):
            if chunk:
                chunk_iters += 1
                local_zip_file.write(chunk)

print(chunk_iters)
