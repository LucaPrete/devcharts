#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import subprocess

from netaddr import IPAddress, IPNetwork

import db
import config
import util

def set_cdn():
	print('\n### Setting values for CDN ###')
	table = config.cdn['table_name']
	tutorial_table = config.cdn['tutorial_table']
	user = config.cdn['user']
	host = config.cdn['host']
	port = config.cdn['port']
	log_path = config.cdn['log_path']
	cdn_files = config.cdn['files']
	cdn_excluded_net = config.cdn['excluded_net']
	date = util.format_date(config.measurement_date)
	result = get_cdn_results(date, user, host, port, log_path, cdn_files, cdn_excluded_net)
	if result and not result == None:
		for key,value in result.iteritems():
			if 'tutorial' in key:
				db.write_to_db(tutorial_table, date, key, value)
			else:
				db.write_to_db(table, date, key, value)

def get_cdn_results(date, user, host, port, path, files, excluded_net):
	# Create the result variable
	result = {}
	# For every filename in the configuration I create a counter and I set it to 0
	for file in files:
		result[file] = 0
	# I put every IP address excluded in the configuration into the right format
	excluded_cidr = [IPNetwork(addr) for addr in excluded_net]
	# I list all the directories (nodes) in the main log directory contained in the config file
	node_list = util.run_remote_cmd(user, host, port, 'ls', path)
	# For each node I check if there's a dir corresponding to the current month
	for node in node_list:
		node = node.rstrip()
		# List directories (dates) contained in a specific node
		date_list = util.run_remote_cmd(user, host, port, 'ls', '%s/%s' % (path, node))
		# Format the today date to return MMYEAR
		folder_date = util.format_date_cdn_ym(date)
		for dates in date_list:
			dates = dates.rstrip()
			# If the current month is in the list of the directories
			if folder_date == dates:
				# List the logs inside the directory
				logs_list = util.run_remote_cmd(user, host, port, 'ls', '%s/%s/%s' % (path, node, folder_date))
				# Format date of today into apache log format (YYYYMMDD) to match on the file name
				log_date = util.format_date_cdn_ymd(date)
				for logs in logs_list:
					logs = logs.rstrip()
					# If a log for today is found
					if log_date in logs:
						# I do bzcat on the log content and I go through it
						log_content = util.run_remote_cmd(user, host, port, 'bzcat', '%s/%s/%s/%s' % (path, node, folder_date, logs))
						# For each line in the log
						for log_lines in log_content.readlines():
							# I split the line on spaces and I save the interesting fields
							log_fields = log_lines.split()
							file_name = log_fields[7]
							ip_address = IPAddress(log_fields[3])
							file_size = log_fields[10]
							bytes_sent = log_fields[11]
							http_req_code = log_fields[9]
							for file in files:
								# Check if the file name contains a file that is in out config
								# Check also that HTTTP code is 200 (request for complete file)
								# Check also that the file was completely transferred
								if file_name == file and http_req_code == '200' and file_size == bytes_sent:
									# Check that the IP of requester was not excluded in the config file
									ip_in_net = False
									for net in excluded_cidr:
										if ip_address in net:
											ip_in_net=True
									# If all the conditions above are satisfied, we can increment
									# the counter for a certain file.
									if ip_in_net == False:
										result[file] = result[file] + 1
	return result
