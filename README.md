# ThingiverseScraper

Scans Thingiverse.com by page ID, captures page details and downloads Thingiverse project files locally.

Dependencies:
* Python 3.6 or later
* MySQL or MariaDB (mariadb-server mariadb-client)
* MySQL Connector for Python (sudo apt-get install python3-mysql.connector)

Steps:
* Create preferred database username and password and add to script
* Set runtime variables
  * Worker start and end ranges
  * Download directory
  * Download buffer size (Currently set to 100MB)
