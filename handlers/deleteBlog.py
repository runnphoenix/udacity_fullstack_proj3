#!/usr/bin/python

from handler import Handler
from google.appengine.ext import db
import functools

import trry

class DeleteBlog(Handler):
	
	@trry.user_logged_in
	@trry.post_exist
	@trry.user_owns_blog
	def get(self, blog_id, blog):
		blog.delete()
		self.redirect('/blog/?')