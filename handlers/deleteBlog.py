#!/usr/bin/python

from handler import Handler
from google.appengine.ext import db
import functools

def blogs_key(name="default"):
	return db.Key.from_path("blogs", name)

class DeleteBlog(Handler):
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
	
	def user_owns_blog(function):
		@functools.wraps(function)
		def wrapper(self, blog_id, blog):
			if self.user.name == blog.author:
				return function(self, blog_id, blog)
			else:
				self.redirect('/blog/%s' % str(blog_id))
				return
		return wrapper
			
	@user_logged_in
	@post_exist
	@user_owns_blog
	def get(self, blog_id, blog):
		blog.delete()
		self.redirect('/blog/?')