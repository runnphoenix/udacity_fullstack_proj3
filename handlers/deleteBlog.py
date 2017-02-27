#!/usr/bin/python

from handler import Handler
from google.appengine.ext import db
import functools

import trry

class DeleteBlog(Handler):
	
	def user_owns_blog(function):
		@functools.wraps(function)
		def wrapper(self, blog_id, blog):
			if self.user.name == blog.user.name:
				return function(self, blog_id, blog)
			else:
				self.redirect('/blog/%s' % str(blog_id))
				return
		return wrapper
			
	@trry.user_logged_in
	@trry.post_exist
	@user_owns_blog
	def get(self, blog_id, blog):
		blog.delete()
		self.redirect('/blog/?')