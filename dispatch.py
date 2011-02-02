#!/usr/bin/env python
# -*- coding: utf-8 -*-

from werkzeug.routing import Map, Rule
from werkzeug import Local, LocalManager

url_map = Map()

local = Local()
local_manager = LocalManager([local])
application = local('application')

_api_prefix = '/_<any(json,xml):api>'

def expose(rule, with_api=True, **kw):
	def decorator(f):
		kw['endpoint'] = f.__name__
		if with_api:
			url_map.add(Rule(_api_prefix + rule, **kw))
		else:
			url_map.add(Rule(rule, **kw))
		return f
	return decorator

def url_for(endpoint, _external=False, **values):
	return local.url_adapter.build(endpoint, values, force_external=_external)

def set2path(s, *args):
	if isinstance(s, set):
		s2 = s.union(args)
	else:
		s2 = s + list(args)
	return u'/'.join((unicode(x) for x in sorted(s2)))

def get_adapter(environ):
	return url_map.bind_to_environ(environ)

