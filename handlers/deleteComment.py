#!/usr/bin/python

from handler import Handler
from models import Comment
from google.appengine.ext import db
import functools

def blogs_key(name="default"):
	return db.Key.from_path("blogs", name)

class DeleteComment(Handler):
	def user_logged_in(function):
		@functools.wraps(function)
		def wrapper(self, *a):
			if self.user:
				return function(self, *a)
			else:
				self.redirect('/login')
				return
		return wrapper
			
	def comment_exist(function):
		@functools.wraps(function)
		def wrapper(self, blog_id, comment_id):
			comment_key = db.Key.from_path("Comment", int(comment_id))
			comment = db.get(comment_key)
			if comment:
				return function(self, blog_id, comment_id)
			else:
				self.error(404)
				return
		return wrapper
	
	# TODO: add user_owns_comment
	
	@user_logged_in
	@comment_exist
	def get(self, blog_id, comment_id):
		comment.delete()
		self.redirect('/blog/%s' % str(blog_id))