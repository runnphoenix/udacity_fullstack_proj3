#!/usr/bin/python

from handler import Handler
from models import Like
from google.appengine.ext import db
import functools

def blogs_key(name="default"):
	return db.Key.from_path("blogs", name)

class LikeBlog(Handler):
	def user_logged_in(function):
		@functools.wraps(function)
		def wrapper(self, *a):
			if self.user:
				return function(self, *a)
			else:
				self.redirect('/login')
				return
		return wrapper
			
	def post_exist(function):
		@functools.wraps(function)
		def wrapper(self, blog_id):
			key = db.Key.from_path("BlogPost", int(blog_id), parent=blogs_key())
			blog = db.get(key)
			if blog:
				return function(self, blog_id, blog)
			else:
				self.error(404)
				return
		return wrapper
		
	@user_logged_in
	@post_exist
	def get(self, blog_id):
		toAdd = True
		like = Like(fromed=self.user.name, blog_id=blog_key.id())
		for liked in blog.likes:
			if liked.fromed == like.fromed:
				toAdd = False
		if toAdd:
			like.put()
			
		self.redirect('/blog/%s' % str(blog_id))