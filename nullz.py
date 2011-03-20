#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from os import path

from werkzeug import Request, Response, SharedDataMiddleware
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import ClosingIterator

#import jinja

from db import Database
import controllers
from dispatch import get_adapter, local, local_manager

import sqlite3

root_path = path.abspath(path.dirname(__file__))

class Application:
	def __init__(self, dbfile):
		local.application = self
		self.db = Database(sqlite3, dbfile)
	
	def __call__(self, environ, start_response):
		#print "__call__"
		local.application = self
		request = Request(environ)
		local.url_adapter = adapter = get_adapter(request.environ)
		
		try:
			endpoint, values = adapter.match()
			print "endpoint=", endpoint
			handler = getattr(controllers, endpoint)
			#try:
			response = handler(request, **values)
			#except Exception as e:
			#	raise NotFound("Nothing here.")
			
		except HTTPException as e:
			response = e
			
		r = response(environ, start_response)
		return ClosingIterator(r, [local_manager.cleanup])

application = Application('0lz.sqlite3')

application = SharedDataMiddleware(application, {
	'/static': path.join(root_path, 'static')
})

if __name__ == '__main__':
	from werkzeug import run_simple
	run_simple('localhost', 4000, application)

