#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys

import db
import config
import util

import analytics_auth

from apiclient.errors import HttpError
from oauth2client.client import AccessTokenRefreshError

def set_analytics():
	print('\n### Setting values for Google Analytics ###')
	for profiles in config.analytics['accounts']:
		print('\n### Processing ' + profiles + ' Google Analytics ###')
		table = config.analytics['accounts'][profiles]['table_name']
		pages = config.analytics['accounts'][profiles]['pages']
		date = util.format_date(config.measurement_date)
		for page in pages:
			# If not, authentication
			service = analytics_auth.initialize_service_analytics()
			# If authenticated, query Google Analytics
			if service:
				account_id = config.analytics['accounts'][profiles]['account_id']
				property_id = config.analytics['accounts'][profiles]['property_id']
				profile_id = config.analytics['accounts'][profiles]['profile_id']
				result = new_data_measurement(service, account_id, property_id, profile_id, date, page)
				# If we get results, write to db
				if result:
					db.write_to_db(table, date, page, result)

def new_data_measurement(service, account_id, property_id, profile_id, date, page):	
	result = None
	try:
		profile_id = get_profile(service, account_id, property_id, profile_id)
		if profile_id:
			result = get_results(service, profile_id, date, 'ga:sessions', page)
	except TypeError, error:
		# Handle errors in constructing a query.
		print ('There was an error in constructing your query : %s' % error)
	except HttpError, error:
		# Handle API errors.
		print ('There was an API error : %s : %s' %
    	(error.resp.status, error._get_reason()))
	except AccessTokenRefreshError:
		# Handle Auth errors.
		print ('The credentials have been revoked or expired, please re-run '
		'the application to re-authorize')
	return result

# Returns the first account from Google Analytics for a specified authenticated user.
def get_profile(service, account_id, property_id, profile_id):
	accounts = service.management().accounts().list().execute()
	if accounts.get('items'):
		for account_ids in accounts.get('items'):
			if unicode(account_id, 'utf-8') in account_ids.values():
				webproperties = service.management().webproperties().list(accountId=account_id).execute()
				if webproperties.get('items'):
					for webproperty_ids in webproperties.get('items'):
						if (unicode('UA-' + account_id + '-' + property_id, 'utf-8')) in webproperty_ids.values():
							profiles = service.management().profiles().list(
        						accountId=account_id,
        						webPropertyId='UA-' + account_id + '-' + property_id).execute()
      							if profiles.get('items'):
				        			return profiles.get('items')[profile_id].get('id')
	return None

# Returns a result of a Google Analytics query, given:
# an auth service, a profile id, a start date, an end date, a metric
# and the name of a specific page (use global for general contacts to website)
def get_results(service, profile_id, date, metrics, page):
	raw_results = service.data().ga().get(
		ids='ga:' + profile_id,
		start_date=date,
		end_date=date,
		metrics=metrics).execute()
	if raw_results and raw_results.get('totalResults')>0:
		return raw_results.get('rows')[0][0]

# Used for debugging. It shows the results of a specific Google Analytics Query
def print_results(results):
	if results and results.get('totalResults')>0:
		print 'First View (Profile): %s' % results.get('profileInfo').get('profileName')
		print 'Total Sessions: %s' % results.get('rows')[0][0]
	
	else:
		print 'No results found'
