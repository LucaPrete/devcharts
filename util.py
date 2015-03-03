#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import os
import subprocess

# Return a te in the following format YY-MM-DD
def format_date(date):
	if date == 'default':
		return '%d-%02d-%02d' % (datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
	else:
		splitted_date = date.split('-')
		year = int(splitted_date[0])
		month = int(splitted_date[1])
		day = int(splitted_date[2])
		return '%d-%02d-%02d' % (year, month, day)

# It formats the date to grep on the Apache logs - the format is dd/Mon/YYYY
def format_date_apache_log(date):
	day = ''
	month = ''
	month_string = ''
	year = ''
	if date == 'default':
		day = str('%02d' % datetime.datetime.now().day)
		month_string = datetime.datetime.now().strftime("%B")[0:3]
		year = str(datetime.datetime.now().year)
	else:
		day = date[8:10]
		month = date[5:7]
		year = date[0:4]
		complete_date = datetime.datetime(int(year), int(month), int(day))
		month_string = complete_date.strftime("%B")[0:3]
	return '%s/%s/%s' % (day, month_string, year)

def format_date_cdn_ym(date):
	month = ''
	year = ''
	if date == 'default':
		month = str('%02d' % datetime.datetime.now().month)
		year = str(datetime.datetime.now().year)
	else:
		month = date[5:7]
		year = date[0:4]
	return '%s%s' % (year, month)

def format_date_cdn_ymd(date):
	month = ''
	year = ''
	if date == 'default':
		day = str('%02d' % datetime.datetime.now().day)
		month = str('%02d' % datetime.datetime.now().month)
		year = str(datetime.datetime.now().year)
	else:
		day = date[8:10]
		month = date[5:7]
		year = date[0:4]
	return '%s%s%s' % (year, month, day)

# It copies a file from a remote location to the local directory.
def copy_file_to_local(user, host, port, path):
	os.system('scp -P %d %s@%s:%s .' % (port, user, host, path))

# It checks if a directory exists or not
def run_remote_cmd(user, host, port, cmd, param):
	ssh = subprocess.Popen(['ssh', '-p %d' % port, '%s@%s' % (user, host), cmd, param],
				stdout=subprocess.PIPE)
	return ssh.stdout
