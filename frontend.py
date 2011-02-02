#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jinja2 as jinja
from werkzeug import Response
import dispatch

def render(name, api, force_plain = False, **values):
	values.update(
		url_for = dispatch.url_for,
		set2path = dispatch.set2path,
	)
	
	t = jinja.Template(open('%s.%s.tmpl' % (name, api), 'r').read())
	if force_plain:
		return Response(t.stream(**values), mimetype='text/plain')
	return Response(t.stream(**values), mimetype='text/%s' % api)

