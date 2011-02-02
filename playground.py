
import db
import sqlite3

d = db.Database(sqlite3, '0lz.sqlite3')

try:
	d.update({
		'url': 'http://leetless.de',
		'title': 'Leetless!',
		'quickmark': 'll',
		'tags': ['programming', 'vim', 'adventure'],
	})
	
	for i in d.get_bookmarks():
		print(i)
finally:
	d.close()
	
