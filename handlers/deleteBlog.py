#!/usr/bin/python

from handler import Handler
from google.appengine.ext import db

def blogs_key(name="default"):
	return db.Key.from_path("blogs", name)

class DeleteBlog(Handler):
	
	def get(self, blog_id):
		blog_key = db.Key.from_path("BlogPost", int(blog_id), parent=blogs_key())
		blog = db.get(blog_key)
	
		blog.delete()
		self.redirect('/blog/?')