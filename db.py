#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import with_statement
from contextlib import contextmanager

import datetime

import psycopg2
import psycopg2.pool

import config
import util

host = config.db['host']
dbname = config.db['dbname']
user = config.db['user']
password = config.db['password']

# create pool with min number of connections of 1, max of 10
dbpool = psycopg2.pool.SimpleConnectionPool(1,5,host=host,dbname=dbname,user=user,password=password)

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
	cur.execute("SELECT EXISTS(SELECT 1 from " + table + " WHERE date=%s AND page=%s) AS exists", [util.format_date(date), page])
	for row in cur.fetchall():
	    return row[0]

# Write a record to a specific table.
def write_to_db(table, date, page, result):
    formatted_date = util.format_date(date)
    with getcursor() as cur:
	cur.execute("SELECT EXISTS(SELECT 1 from " + table + " WHERE date=%s AND page=%s) AS exists", [formatted_date, page])
	for row in cur.fetchall():
	    if not row[0]:
		cur.execute("INSERT INTO " + table + "(date,sessions,page) VALUES (%s,%s,%s)", [formatted_date, result, page])
	    else:
		cur.execute("UPDATE " + table + " SET sessions=%s WHERE date=%s AND page=%s", [result, formatted_date, page])

# Register a commit in a specific table in the DB.
def write_git_commits_to_db(table, date, dev_name, commits, lines_added, lines_removed):
    formatted_date = util.format_date(date)
    with getcursor() as cur:
	cur.execute("SELECT commits, lines_added, lines_removed from " + table +
		" WHERE date=%s AND dev_name=%s", [formatted_date, dev_name])
	for row in cur.fetchall():
	    if not row[0]:
			cur.execute("INSERT INTO " + table + """(date, commits, dev_name, lines_added,
				lines_removed) VALUES (%s, %s, %s, %s, %s)""", [formatted_date, commits,
				dev_name, lines_added, lines_removed])
	    else:
	    	cur.execute("UPDATE " + table + """ SET commits=%d, lines_added=%d,
			    lines_removed=%d WHERE date=%s AND dev_name=%s""",
			    [commmits, lines_added, lines_removed, formatted_date, dev_name])


# Get all data from a specific table, given a date and a specific page
def get_from_db(table, titles=['Interactions']):
    with getcursor() as cur:
        cur.execute("SELECT * FROM " + table + " ORDER BY date")
        date_col = {'id':'date', 'label':'Date', 'pattern':'MMM yyyy', 'type':'date', 'role':'domain'}
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