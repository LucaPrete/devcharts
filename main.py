#!/usr/bin/python
# -*- coding: utf-8 -*-

import analytics
import youtube
import gerrit
import cdn
import git

def main():
	analytics.set_analytics()
	youtube.set_analytics()
	gerrit.set_gerrit()
	git.set_git()
	cdn.set_cdn()
	print('\n')
	
if __name__ == "__main__":
    main()
