# ThingiverseScraper

Disclaimer: This is a thought experiment and is for educational purposes. The author takes no responsibility for the misuse of these scripts as this disclaimer implies a "No Jerk" policy when automating websites visits.

Scans Thingiverse.com by page ID, captures page details and downloads Thingiverse project files locally.

Dependencies:
* Python 3.6 or later
* MySQL or MariaDB (mariadb-server mariadb-client)
* MySQL Connector for Python (sudo apt-get install python3-mysql.connector)

Steps:
* Create preferred database username and password and add to script
* Load "thingiverse_catalog" into database
* Set runtime variables
  * Worker start and end ranges
  * Download directory
  * Download buffer size (Currently set to 100MB)
