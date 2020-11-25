# ThingiverseScraper

Disclaimer: This is a thought experiment and is for educational purposes. The author takes no responsibility for the misuse of these scripts.

This application can be used to systematically scrape content (HTML and files) from thingiverse.com

Dependencies:
* No dependencies (requests and sqlite3 are currently part of Python 3.8 standard library)

Steps:
* Run setup_thingiverse_database.py to create database for storage
* Define configuration variables at the top of thingiverse_scraper.py
* Run thingiverse_scraper.py and get a coffee (This will take a real long time...)

Structure:
* Thingiverse_scraper will create two new directories within its directory 'files' and 'html' to capture Thingiverse Thing zip files and the Thing's HTML page source, respectively. This allows for the user to dig into the page source for items like 'tags' or other interesting information per thing.
