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
The tool is made of two main components:
- The ones that are used to collect periodically data and save them into the database (files contained in the back-end directory).
- The ones that are used to load the data contained in the database and visualize them in a webpage through Google Charts tables and charts (index.html file contained in the front-end directory).

# Notes for back-end python files:
Python was used because it's easy to use and read, and because it easly triggerable from the Linux CLI as well. Specially, it is very easy in this case, to schedule the collection of the data from - i.e. - the crontab.

# Notes for index.html file:
The file can be extended, depending from
- The general structure of the webpage
- The CSS style applied to the page
- Components can be added and removed from the standard example structure provided, depending on the number of
  components that need to be shown in the web gui.
- Substitute the parameters {...} with the values you want

# Working examples:
Currently the tool is used to track hourly the statistics for the ONOS open source project (www.onosproject.org). The final result can be viewed here: http://stats.onosproject.org
