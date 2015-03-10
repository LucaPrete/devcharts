# devcharts
The system enables a user to keep track of different statistics and visualize them in a web-page through Google Charts.
Specifically, the system enables you to track:

- Number of Gerrit clones
- Number of Git commits for a certain repository
- Page views and website accesses through Google Analytics
- Number of YouTube video views

The tool allows to report statistics per day and per month, draw tables and per-day aggregate charts.

# Requirements:
- Python 2.7
- Any webserver (i.e. Apache)
- PostreSQL 9.X

# Components and folders:
- Back-end: Python files to periodically collect new data and save them in the database.
- Front-end: The directory contains the file used to visualize the statistics.
