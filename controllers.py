#!/usr/bin/env python
# -*- coding: utf-8 -*-

from frontend import render
from database import Bookmark
from dispatch import expose, url_for, set2path, local, local_manager
from werkzeug import redirect, Response
from werkzeug.exceptions import NotFound

app = local('application')

@expose('/<quickmark>', with_api=False)
def get_quickmark(request, quickmark):
	bm = tuple(app.db.get_bookmarks(quickmark = quickmark))
	if not len(bm):
		raise NotFound
	return redirect(bm[0]['url'])

@expose('/bookmark/<id>', methods=('POST',))
def edit_bookmark(request, api, id):
	print("----------------")
	action = request.form['action']
	
	print(request.form)
	if action == 'delete':
		print("deleting")
		app.db.delete_bookmark(id)
		print("deleted")
		return render('status', api,
			status = 'acknowledged',
			operation = 'delete',
			bookmark_id = id,
		)

@expose('/bookmarks/<path:tags>', methods=('POST',))
def edit_bookmarks(request, api, tags):
	action = request.form['action']
	tags = set((x for x in tags.split('/') if x))
	
	if action == 'add':
		b = {
			'url': request.form['url'],
			'title': request.form['title'],
			'tags': tags,
			'quickmark': request.form.get('quickmark', ''),
		}
		app.db.update(b)
		return render('status', api,
			status = 'acknowledged',
			force_plain = True,
			operation = 'add',
			subject = 'bookmark',
			detail_id = '',        # <- TODO
			detail_url = b['url'],
			detail_title = b['title']
		)

@expose('/bookmarks/<path:tags>', methods=('GET',))
def get_bookmarks(request, api, tags):
	"""
	"""
	tags = list(set((x for x in tags.split('/') if x)))
	tags.sort()
	bookmarks = list(app.db.get_bookmarks(tags=tags))
	bookmarks.sort()
	return render('bookmarks', api,
		tags = tags,
		bookmarks = bookmarks,
	)

@expose('/tags')
@expose('/tags/')
def get_tag_index(request, api):
	"""
	"""
	return get_tags(request, api, '')

@expose('/tags/<path:tags>')
def get_tags(request, api, tags):
	"""
	"""
	tags = set((x for x in tags.split('/') if x))
	
	bookmarks = list(app.db.get_bookmarks(tags=tags))
	bookmarks.sort()
	
	subtags = {} # tag -> bookmark
	for bm in bookmarks:
		for t in bm['tags']:
			if t not in tags:
				subtags[t] = subtags.get(t, 0) + 1
	
	tags = list(tags)
	tags.sort()
	def iter_subtags():
		ks = list(subtags.keys())
		ks.sort()
		for tag in ks:
			count = subtags[tag]
			d = dict(
				tags = set2path(tags, tag),
				api = api
			)
			yield dict(
				name = tag,
				bookmark_count = count,
				bookmarks_url = url_for('get_bookmarks', **d),
				tags_url = url_for('get_tags', **d)
			)
	
	return render('subtags', api,
		bookmark_count = len(bookmarks),
		tags = tags,
		subtags = iter_subtags(),
	)

