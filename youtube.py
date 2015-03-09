#!/usr/bin/python

from datetime import datetime, timedelta

import analytics_auth
import config
import db
import httplib2
import os
import sys
import util

from apiclient.discovery import build
from oauth2client.file import Storage
from optparse import OptionParser

def set_analytics():
	print('\n### Setting values for Youtube Analytics ###')
	# Setting date of today and different user configuration options
	date = util.format_date(config.measurement_date)
	table = config.youtube['table_name']
	youtube_channel_id = config.youtube['channel_id']
	service = analytics_auth.initialize_service_youtube()
	# Loading authentication services for youtube and youtube analytics.
	youtube = service['youtube']
	youtube_analytics = service['youtube_analytics']
	youtube_parser = create_youtube_parser(date)
	# Get the list of user youtube channels
	channels = get_channels_list(youtube, youtube_channel_id)
	for channel in channels.get("items", []):
		# For each channel get the analytics for all videos
		results = get_video_analytics(youtube_analytics, channel['id'], youtube_parser)
	if results and len(results)>0: 
		for result in results:
			# print('Result: video id => %s, views => %s' % (result[0], result[1]))
			db.write_to_db(table, date, result[0], result[1])

# Returns a channel list
def get_channels_list(youtube_service, channel_id):
	return youtube_service.channels().list(id=channel_id, part="id").execute()

# Returns a Youtube parser to get the results
def create_youtube_parser(date):
	parser = OptionParser()
	parser.add_option("--metrics", dest="metrics", help="Report metrics",
  		default="views")
	parser.add_option("--dimensions", dest="dimensions", help="Report dimensions",
  		default="video")
	parser.add_option("--start-date", dest="start_date",
  		help="Start date, in YYYY-MM-DD format", default=date)
	parser.add_option("--end-date", dest="end_date",
  		help="End date, in YYYY-MM-DD format", default=date)
	parser.add_option("--start-index", dest="start_index", help="Start index",
  		default=1, type="int")
	parser.add_option("--max-results", dest="max_results", help="Max results",
  		default=10, type="int")
	parser.add_option("--sort", dest="sort", help="Sort order", default="-views")
	(options, args) = parser.parse_args()
	return options

# Returns analytics about videos in a specific channel, given an Analytics service,
# a channel Id and a Youtube parser
def get_video_analytics(youtube_analytics_service, channel_id, options):
	analytics_response = youtube_analytics_service.reports().query(
    	ids="channel==%s" % channel_id,
    	metrics=options.metrics,
    	dimensions=options.dimensions,
    	start_date=options.start_date,
    	end_date=options.end_date,
    	start_index=options.start_index,
    	max_results=options.max_results,
    	sort=options.sort
		).execute()
	return analytics_response.get("rows", [])
