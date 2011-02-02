
from threading import Lock, Thread
try:
	from queue import Queue, Empty
except ImportError:
	from Queue import Queue, Empty


class Database(object):
	thread_ = None
	thread_lock_ = Lock()
	
	def __init__(self, db, *args, **kws):
		self.db = db
		self.db_args = args
		self.db_kws = kws
	
	def check_thread(self):
		with Database.thread_lock_:
			if Database.thread_ and not Database.thread_.is_alive():
				Database.thread_ = None
				
			if not Database.thread_:
				Database.thread_ = DatabaseThread(self.db, self.db_args, self.db_kws)
				Database.thread_.daemon = False
				Database.thread_.start()
				
	def close(self):
		self.check_thread()
		Database.thread_.close()
	
	def execute(self, query, args):
		self.check_thread()
		Database.thread_.execute(query, args)
		
	def select(self, query, args):
		self.check_thread()
		return Database.thread_.select(query, args)
	
	def get_tags(self, bookmark_id=None):
		if bookmark_id:
			iter = self.select(
				'select tag_name from tag where tag.bookmark_id=? group by tag_name',
				(bookmark_id,)
			)
			for i in iter:
				yield i[0]
	
	def get_bookmarks(self, url=None, id=None, quickmark=None, tags=()):
		where = ''
		args = []
		
		if url:
			where += 'url=? '
			args.append(url)
			
		if id:
			if where: where += 'and '
			where += 'id=? '
			args.append(id)
			
		if quickmark:
			if where: where += 'and '
			where += 'quickmark=? '
			args.append(quickmark)
		
		for tag in tags:
			if where: where += 'and '
			where += 'exists(select * from tag where tag.tag_name=? and tag.bookmark_id = bookmark.id) '
			args.append(tag)
		
		iter = self.select(
			'select bookmark.id, bookmark.url, bookmark.title, bookmark.quickmark ' +
			'from bookmark ' +
			('where ' + where if where else '') +
			'group by bookmark.id, bookmark.url, bookmark.title, bookmark.quickmark '
			,
			args
		)
		
		for i in iter:
			yield {
				'id': i[0],
				'url': i[1],
				'title': i[2],
				'quickmark': i[3],
				'tags': set(self.get_tags(bookmark_id=i[0])),
			}
		
	def delete_bookmark(self, id):
		self.execute('delete from tag where bookmark_id=?', (id,))
		self.execute('delete from bookmark where id=?', (id,))
	
	def update(self, bookmark):
		old = None
		
		if 'id' in bookmark:
			r = tuple(self.get_bookmarks(id=bookmark['id']))
			if len(r): old = r[0]
		elif 'url' in bookmark:
			r = tuple(self.get_bookmarks(url=bookmark['url']))
			if len(r): old = r[0]
	
		if old: # UPDATE
			to_remove = set(old['tags']) - set(bookmark.get('tags', ()))
			to_add = set(bookmark.get('tags', ())) - set(old['tags'])
			
			for tag_name in to_remove:
				self.execute(
					'delete from tag where tag_name=? and bookmark_id=?',
					(tag_name, old['id'])
				)
			for tag_name in to_add:
				self.execute(
					'insert into tag (tag_name, bookmark_id) values (?, ?)',
					(tag_name, old['id'])
				)
			
			self.execute(
				'update bookmark set url=?, title=?,  quickmark=? where id=?',
				(
					bookmark.get('url', old['url']),
					bookmark.get('title', old['title']),
					bookmark.get('quickmark', old['quickmark']) or None,
					old['id']
				)
			)
			
		else: # INSERT
			self.execute(
				'insert into bookmark (url, title, quickmark) values (?, ?, ?)',
				(
					bookmark['url'],
					bookmark.get('title', bookmark['url']),
					bookmark.get('quickmark') or None
				)
			)
			for bm in self.select('select id from bookmark where url=?', (bookmark['url'],)):
				for tag in bookmark['tags']:
					self.execute(
						'insert into tag (bookmark_id, tag_name) values (?, ?)',
						(bm[0], tag)
					)
					

class DatabaseThread(Thread):
	
	class Close: pass
	class End: pass
	
	def __init__(self, db, db_args, db_kws):
		Thread.__init__(self)
		self.db = db
		self.db_args = db_args
		self.db_kws = db_kws
		self.tasks = Queue()
	
	def execute(self, query, args, result=None):
		self.tasks.put((query, args, result))
	
	def select(self, query, args):
		result = Queue()
		self.execute(query, args, result)
		r = None
		while True:
			r = result.get(True, 5)
			if r is self.End:
				break
			yield r
	
	def close(self):
		self.tasks.put((self.Close, None, None))
		
	def run(self):
		try:
			connection = self.db.connect(*self.db_args, **self.db_kws)
			cursor = connection.cursor()
			while True:
				try:
					query, args, result = self.tasks.get(True, 20)
				except Empty:
					continue
				
				if query is self.Close: break
				
				print("EXECUTING:", query)
				cursor.execute(query, args)
				connection.commit()
				if result:
					for row in cursor:
						result.put(row)
					result.put(self.End)
					
		finally:
			connection.close()

