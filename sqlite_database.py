
from threading import Lock, Thread
from Queue import Queue

class Database(object):
	thread_ = None
	thread_lock_ = Lock()
	
	def __init__(self, db, *args, **kws):
		self.db = db
		self.db_args = args
		self.db_kws = kws
		
	def check_thread(self):
		with Database.thread_lock_
			if not Database.thread_:
				Database.thread_ = DatabaseThread(self.db, *self.db_args, **self.db_kws)
			if not Database.thread_.is_alive():
				Database.thread_.start()
		
	def get_bookmarks(self, url=None, id=None, tags=()):
		#self.connection.execute(...)
	
	def update(self, bookmark):
		#

class DatabaseThread(Thread):
	def __init__(self, db, db_args, db_kws):
		self.db = db
		self.db_args = db_args
		self.db_kws = db_kws
		self.tasks = Queue()
	
	def execute(self, query, result=None):
		self.tasks.put((query, result))
	
	def select(self, query):
		result = Queue()
		self.execute(query, result)
		return result.get()
		
	def run(self):
		connection = db.connect(**self.db_args, **self.db_kws)
		cursor = connection.cursor
		while True:
			query, result = self.tasks.get()
			cursor.execute(query, args)
			if result:
				for row in cursor:
					result.put(dict(row))

