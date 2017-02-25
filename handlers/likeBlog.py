#!/usr/bin/python

from handler import Handler
from models import Like
from google.appengine.ext import db

def blogs_key(name="default"):
	return db.Key.from_path("blogs", name)

class LikeBlog(Handler):
	
	def get(self, blog_id):
		blog_key = db.Key.from_path("BlogPost", int(blog_id), parent=blogs_key())
		blog = db.get(blog_key)
	
		toAdd = True
		like = Like(fromed=self.user.name, blog_id=blog_key.id())
		for liked in blog.likes:
			if liked.fromed == like.fromed:
				toAdd = False
		if toAdd:
			like.put()
			
		self.redirect('/blog/%s' % str(blog_id))