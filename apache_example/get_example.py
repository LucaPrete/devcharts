#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp2
import config

# import db: this refers to the db file contained in the backend directory of the repository.
If your file is not in the same folder of this file, put its absolute path.
import db

import json

class first_class(webapp2.RequestHandler):

    def get(self, table):
        output = json.dumps(db.get_from_db(table))
        self.response.headers['Content-type'] = 'application/json;charset=utf-8'
        self.response.out.write(output)

class second_class(webapp2.RequestHandler):

    def get(self, table):
        output = json.dumps(db.get_from_db(table))
        self.response.headers['Content-type'] = 'application/json;charset=utf-8'
        self.response.out.write(output)

routes = [
    # This is to map requests arriving to the wsgi application to a specific class.
    # If you've different paths you can put here multiple lines separated by commas.
    # Here are just some examples. In both of the cases the final parth of the URI (one, two, three)
    # will be also the name of the table (parameter passed to the class) to get the correct data from the correct table 
    # Reqests to server_address.xxx/stats/one or server_address.xxx/stats/two will be mapped to the class first_class
    (r'/stats/(one|two)',first_class),
    # Reqests to server_address.xxx/stats/three will be mapped to the class second_class
    (r'/stats/(three)',second_class)
]

application = webapp2.WSGIApplication(routes=routes, debug=False)
