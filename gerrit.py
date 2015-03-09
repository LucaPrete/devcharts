#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import re

import db
import config
import util

def set_gerrit():
	print('\n### Setting values for Gerrit ###')
	user = config.gerrit['user']
	host = config.gerrit['host']
	port = config.gerrit['port']
	path = config.gerrit['log_path']
	table = config.gerrit['table_name']
	date = util.format_date(config.measurement_date)
	result = get_gerrit_contacts(date, host, port, user, path)
	if result:
		db.write_to_db(table, date, 'global', result)

def get_gerrit_contacts(date, host, port, user, log_path):
	# Format the date for apache.
	formatted_date = util.format_date_apache_log(date)
	# Declare empty array which will be filled with IPs observed today.
	today_contacts = []
	# Check for new contacts in the last log files
	log_files = util.run_remote_cmd(user, host, port, 'ls', '%s' % (log_path))
	for files in log_files:
		if files.startswith('other_vhosts_access') and files.rstrip().split('.')[-1]!='gz':
			ssh_output = util.run_remote_cmd(user, host, port, 'sudo cat', '%s/%s' % (log_path, files))
			today_contacts = filter_contacts(formatted_date, ssh_output, today_contacts)
	# Is there any old archive of logs in the same directory?
	for files in log_files:
		if files.startswith('other_vhosts_access') and files.rstrip().endswith('gz'):
			ssh_output = util.run_remote_cmd(user, host, port, 'sudo zcat', '%s/other_vhosts_access.log.%d.gz' % (log_path, i))
			today_contacts = filter_contacts(formatted_date, ssh_output, today_contacts)
	# Return the number of contacts found
	return len(today_contacts)

def filter_contacts(date, ssh_output, contacts):
	for text in ssh_output:
		if date in text:
			text = text.rstrip()
			regex = re.findall( r'[0-9]+(?:\.[0-9]+){3}', text )
			if len(regex)>0 and regex is not None:
				value = str(regex[0])
				if value not in contacts:
					contacts.append(value)
	return contacts
