#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement
from contextlib import contextmanager

import datetime

import decimal

import psycopg2
import psycopg2.pool

import config
import util

host = config.db['host']
dbname = config.db['dbname']
user = config.db['user']
password = config.db['password']

# create pool with min number of connections of 1, max of 10
dbpool = psycopg2.pool.SimpleConnectionPool(1, 5, host=host, dbname=dbname,
	user=user,password=password)

@contextmanager
def getcursor():
    con = dbpool.getconn()
    con.autocommit = True
    try:
        yield con.cursor()
    finally:
    	dbpool.putconn(con)

# Check if a record with the date of today already exists in a table (Not currently used)
def db_key_exists(table, date, page):
    with getcursor() as cur:
	cur.execute("SELECT EXISTS(SELECT 1 from " + table + """ WHERE date=%s AND page=%s)
		AS exists""", [util.format_date(date), page])
	for row in cur.fetchall():
	    return row[0]

# Write a record to a specific table.
def write_to_db(table, date, page, result):
    formatted_date = util.format_date(date)
    with getcursor() as cur:
	cur.execute("SELECT EXISTS(SELECT 1 from " + table + """ WHERE date=%s AND page=%s)
		AS exists""", [formatted_date, page])
	for row in cur.fetchall():
	    if not row[0]:
		cur.execute("INSERT INTO " + table + "(date,sessions,page) VALUES (%s,%s,%s)",
			[formatted_date, result, page])
	    else:
		cur.execute("UPDATE " + table + " SET sessions=%s WHERE date=%s AND page=%s",
			[result, formatted_date, page])

# Register a commit in a specific table in the DB.
def write_git_commits_to_db(table, date, dev_name, commits, lines_added, lines_removed):
    formatted_date = util.format_date(date)
    with getcursor() as cur:
	cur.execute("SELECT EXISTS(SELECT 1 FROM " + table + """  WHERE date=%s AND 
		 dev_name=%s) AS exists""", [formatted_date, dev_name])
	for row in cur.fetchall():
	    if not row[0]:
	    	cur.execute("INSERT INTO " + table + """(date, commits, dev_name, lines_added,
				lines_removed) VALUES (%s, %s, %s, %s, %s)""", [formatted_date, commits,
				dev_name, lines_added, lines_removed])
	    else:
	    	cur.execute("UPDATE " + table + """ SET commits=%s, lines_added=%s,
			    lines_removed=%s WHERE date=%s AND dev_name=%s""",
			    [commits, lines_added, lines_removed, formatted_date, dev_name])

# Get all data from a specific table, given a date and a specific page
def get_from_db(table, titles=['Interactions']):
    with getcursor() as cur:
        cur.execute("SELECT * FROM " + table + " ORDER BY date")
        date_col = {
        	'id':'date',
        	'label':'Date',
        	'pattern':'MMM yyyy',
        	'type':'date',
        	'role':'domain'
        }
        cols = [date_col]
        for title in titles:
	    	cols.append({'id':title.lower(), 'label':title, 'type':'number', 'role':'data'})
        rows = []
        for row in cur.fetchall():
            date = {'v': 'Date(%d, %d, %d)' % (row[0].year, row[0].month-1, row[0].day)}
            row_list = [date]
	    for i in range(1, len(titles)+1):
	        if row[i] == None:
		    sessions = {'v': 0}
		else:
		    sessions = {'v': int(row[i])}
                row_list.append(sessions)
	    item = {'c': row_list}
            rows.append(item)
        result = {'cols': cols, 'rows':rows}
        return result

# The method is used to retrieve data for making a data table
# The first DB column must be of type string, the other types can be numbers
# Get all data from a specific table, given a date and a specific page
def get_table_from_db(table, titles=['Item', 'Interactions']):
    with getcursor() as cur:
        restults = []
        db_results = []
        cols = []
        rows = []
        cur.execute("SELECT * FROM " + table)
        for row in cur.fetchall():
        	db_results.append(row)
        first_row = db_results[1]
        for i in range(0, len(titles)):
        	col_value = build_col_value(titles[i], first_row[i])
        	cols.append(col_value)
        for result in db_results:
            rows_values_list = []
            rows_values_dict = {}
            for i in range(0, len(titles)):
                row_value = build_row_value(result[i])
                rows_values_list.append(row_value)
            rows_values_dict['c'] = rows_values_list
            rows.append(rows_values_dict)
        return {'cols': cols, 'rows':rows}

# Get all data from a specific table, given a date and a specific page
def get_data_from_db(table, titles=['Date', 'Interactions']):
    with getcursor() as cur:
        restults = []
        db_results = []
        cols = []
        rows = []
        cur.execute("SELECT * FROM " + table + " ORDER BY date")
        for row in cur.fetchall():
        	db_results.append(row)
        first_row = db_results[0]
        for i in range(0, len(titles)):
        	col_value = build_col_value(titles[i], first_row[i])
        	# print(type(first_row[i]))
        	# print(build_col_value('prova - ', first_row[i]))
        	cols.append(col_value)
        for result in db_results:
            rows_values_list = []
            rows_values_dict = {}
            for i in range(0, len(titles)):
                row_value = build_row_value(result[i])
                rows_values_list.append(row_value)
            rows_values_dict['c'] = rows_values_list
            rows.append(rows_values_dict)
        return {'cols': cols, 'rows':rows}

# Get all data from a specific table, given a date and keeping original titles
def get_data_from_db_def_titles(table):
    with getcursor() as cur:
        restults = []
        db_results = []
        cols = []
        rows = []
        cur.execute("SELECT * FROM " + table + " ORDER BY date")
        for row in cur.fetchall():
        	db_results.append(row)
        first_row = db_results[0]
        titles = [desc[0] for desc in cur.description]
        for i in range(0, len(titles)):
        	col_value = build_col_value(titles[i], first_row[i])
        	#print(type(first_row[i]))
        	#print(build_col_value('prova - ', first_row[i]))
        	cols.append(col_value)
        for result in db_results:
            rows_values_list = []
            rows_values_dict = {}
            for i in range(0, len(titles)):
                row_value = build_row_value(result[i])
                rows_values_list.append(row_value)
            rows_values_dict['c'] = rows_values_list
            rows.append(rows_values_dict)
        return {'cols': cols, 'rows':rows}

# Returns the value of a column in the accepted JSON Google charts format.
# Depending on the data type in input the column will be considered either
# as type number or string. 
def build_col_value(col_title, row_value):
    result = None
    if isinstance(row_value, decimal.Decimal) or isinstance(row_value, int) or isinstance(row_value, long):
        result = {'id':col_title.lower(), 'label':col_title, 'type':'number'}
    elif isinstance(row_value, datetime.date):
    	result = {'id':'date', 'label':'Date', 'type':'date', 'pattern':'MMM yyyy'}
    elif row_value == None:
    	result = {'id':col_title.lower(), 'label':col_title, 'type':'number'}
    else:
        result = {'id':col_title.lower(), 'label':col_title, 'type':'string'}
    return result

# Returns the value of a row in the accepted JSON Google charts format.
# Give a value X in input, if the value is not None it will be returned {'v': X}.
# If the value is None it will be returned {'v': 0} or numbers and {'v': ''} for strings.
def build_row_value(row_value):
    result = None
    if isinstance(row_value, decimal.Decimal) or isinstance(row_value, int) or isinstance(row_value, long):
        result = {'v': int(row_value)}
    elif isinstance(row_value, datetime.date):
        result = {'v': 'Date(%d, %d, %d)' % 
            (row_value.year, row_value.month-1, row_value.day)}
    elif row_value == None:
    	result = {'v': int(0)}
    else:
        result = {'v': str(row_value)}
    return result
