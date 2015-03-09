#!/usr/bin/python
# -*- coding: utf-8 -*-

from github import Github

import db
import config
import util
import datetime

def set_git():
	print('\n### Setting values for Git ###')
	repo_full_name = config.git['repo_full_name']
	table = config.git['table_name']
	user = config.git['user']
	pwd = config.git['pass']
	date = util.format_date(config.measurement_date)
	python_start_date = datetime.datetime.strptime('%s 0:0:0' % date, '%Y-%m-%d %H:%M:%S')
	python_end_date = datetime.datetime.strptime('%s 23:59:59' % date, '%Y-%m-%d %H:%M:%S')
	results = get_git_results(user, pwd, repo_full_name, python_start_date, python_end_date)
	if results:
		for author, counters in results.iteritems():
			db.write_git_commits_to_db(table, date, author, counters['commits'],
				counters['lines_added'], counters['lines_removed'])

def get_git_results(git_user, git_pwd, git_repo, start_date, end_date):
	git = Github(git_user, git_pwd)
	git_repo = git.get_repo(git_repo)
	commits = git_repo.get_commits(since=start_date, until=end_date)
	results = {}
	for commit in commits:
		author = 'Unrecognized user'
		if commit.author != None:
			if commit.author.name != None:
				author = commit.author.name
			elif commit.author.login != None:
				author = commit.author.login
		lines_added = commit.stats.additions
		lines_removed = commit.stats.deletions
		# print('Author: %s ' % author)
		# print('Lines added: %s ' % lines_added)
		# print('Lines removed: %s ' % lines_removed)
		if not author in results:
			results[author] = {
				'commits': 1,
				'lines_added': lines_added,
				'lines_removed': lines_removed
			}
		else:
			results[author] = {
				'commits': results[author]['commits']+1,
				'lines_added': results[author]['lines_added']+lines_added,
				'lines_removed': results[author]['lines_removed']+lines_removed,
			}
	return results
