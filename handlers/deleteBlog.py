#!/usr/bin/python

from handler import Handler
from google.appengine.ext import db
import functools

import accessControl

class DeleteBlog(Handler):
	
	@accessControl.user_owns_blog
	@accessControl.post_exist
	@accessControl.user_logged_in
	def get(self, blog_id, blog):
		blog.delete()
		self.redirect('/blog/?')