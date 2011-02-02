
from threading import Lock

class Database:
	def __init__(self, filename):
		self._file_lock = Lock()
		self._filename = filename
		Bookmark.db = self
		self._load()
		
	def _load(self):
		with self._file_lock:
			self._by_id = {}
			self._by_tag = {}
			
			title_by_url = {}
			
			for line in open(self._filename + '.titles', 'r'):
				line = line.decode('utf-8')
				line = line.strip()
				if line.startswith('#'): continue
				l = line.split(None, 1)
				if len(l) < 2: continue
				url = l[0]
				title = l[1]
				title_by_url[url] = title
				
			
			for line in open(self._filename, 'r'):
				line = line.decode('utf-8')
				line = line.strip()
				if line.startswith('#'): continue
				l = line.split()
				if len(l) < 2: l = (l[0], '_untagged')
				url = l[0]
				
				bookmark = Bookmark(url)
				bookmark.title = title_by_url.get(url, '')
				self._insert(bookmark, l[1:])
				bookmark.ensure_id()
			
	def _save(self):
		with self._file_lock:
			f = open(self._filename, 'w')
			ft = open(self._filename + '.titles', 'w')
			print "saving:", self._by_id
			for id, bookmark in self._by_id.items():
				l = u'%s\t%s %s\n' % (bookmark.url, ' '.join(bookmark.tags), bookmark.id)
				f.write(l.encode('utf-8'))
				ft.write((u'%s\t%s\n' % (bookmark.url, bookmark.title)).encode('utf-8'))
			ft.close()
			f.close()
			
			
	def _is_id(self, s):
		return s.isdigit()
	
	def _insert(self, bookmark, tags):
		print "_insert(%s, %s)" % (bookmark, tags)
		for tag in tags:
			if self._is_id(tag):
				bookmark.id = tag
				self._by_id[tag] = bookmark
			else:
				if not tag: continue
				if tag not in self._by_tag:
					self._by_tag[tag] = set()
				self._by_tag[tag].add(bookmark)
				bookmark.tags.add(tag)
		
		bookmark.ensure_id()
		self._by_id[bookmark.id] = bookmark
		print "_by_tag=", self._by_tag
	
	def insert(self, bookmark, tags):
		self._insert(bookmark, tags)
		self._save()
	
	def get_bookmarks_by_tags(self, tags):
		"""
		Given an iterable of tags, return an iterable of bookmark objects.
		tags must contain at least one tag.
		"""
		if not tags:
			s = set()
			for v in self._by_tag.values():
				s.update(v)
			
		else:
			iter = tags.__iter__()
			s = self._by_tag.get(iter.next(), set())
			for t in iter:
				s = s.intersection(self._by_tag.get(t, set()))
		return s
	
	def get_bookmark_by_id(self, id):
		"""
		"""
		return self._by_id[str(id)]

class Bookmark:
	db = None
	max_id = 0
	
	def __init__(self, url):
		self.url = url
		self._id = None
		self.tags = set()
		self.title = ''
	
	def get_id(self):
		return self._id
	
	def set_id(self, id):
		self._id = id
		if self._id > Bookmark.max_id:
			Bookmark.max_id = self._id
			
	id = property(get_id, set_id)
	
	def ensure_id(self):
		if self._id is None:
			Bookmark.max_id += 1
			self._id = Bookmark.max_id
			
	def __repr__(self):
		return self.url
		
	@classmethod
	def delete(cls, id):
		# TODO
		return
	
	@classmethod
	def insert(cls, b, tags):
		return cls.db.insert(b, tags)
	
	@classmethod
	def get_by_tags(cls, tags):
		return cls.db.get_bookmarks_by_tags(tags)
	
	@classmethod
	def get(cls, id):
		return cls.db.get_bookmark_by_id(id)
