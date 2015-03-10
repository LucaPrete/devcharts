#!/usr/bin/python
# -*- coding: utf-8 -*-

db = {
	'host':'{db hostname}',
	'dbname':'{db port}',
	'user':'{db user}',
	'password':'{db pass}'
}

analytics = {
	'p12_path': '{google p12 key file}',
	'service_user': '{google service account user}',
	'scope': 'https://www.googleapis.com/auth/analytics.readonly',
	'api_service_name': 'analytics',
	'api_version': 'v3',
	'accounts': {
		'{arbitrary name of object to be tracked in google analytics. Could be i.e. foo}': {
			'table_name': '{name of the table where to save data in the db}',
			'account_id': '{Google analytics account id number}',
			'property_id': '{property number in google analytics}',
			'profile_id': 0,
			'pages': ['{Arabitrary name of a page to be written in the database, in the page column, for this object}']
		}
		# Here more objects to be tracked an be inserted.
	}
}

youtube = {
	'table_name': '{name of the table where to save data in the db}',
	'secrets_file': '{absolute path to your google secret file}',
	'oauth_warning_msg': 'WARNING: Please configure OAuth 2.0',
	'youtube_api_service_name': 'youtube',
	'youtube_api_version': 'v3',
	'youtube_analytics_api_service_name': 'youtubeAnalytics',
	'youtube_analytics_api_version': 'v1',
	'youtube_scopes': [
		"https://www.googleapis.com/auth/youtube.readonly",
  		"https://www.googleapis.com/auth/yt-analytics.readonly"
  	],
  	'channel_id': '{your youtube channel id}'
}

gerrit = {
	'table_name': '{name of the table where to save data in the db}',
	'host': '{host address}',
	'port': {ssh port on the host},
	'user': '{username on the host, able to have read access to the specified apache log folder}',
	'log_path': '{absolute path of the directory containing the log files}'
}

git = {
	'table_name': '{name of the table where to save data in the db}',
	'repo_full_name': '{full repository name}',
	'user': '{github username}',
	'pass': '{github password}'
}

cdn = {
	'table_name': '{name of the table where to save data in the db}',
	'tutorial_table': 'cdn_tutorial_day',
	'host': '{host address}',
	'port': {ssh port on the host},
	'user': '{username on the host, able to have read access to the specified apache log folder}',
	'log_path': '{absolute path of the directory containing the log files}',
	'excluded_net': [],
	'files': [{comma separated values of absolut path to the tar.gz log files. i.e. 'log1.tar.gz', 'log2.tar.gz', ...}],
}

# Specify the date for a specific day to collect data for.
# Use default for today, use YY-MM-DD for another specific day
measurement_date = 'default'
