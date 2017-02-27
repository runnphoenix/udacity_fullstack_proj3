#!/usr/bin/python

from handler import Handler
from models import Comment
from google.appengine.ext import db
import functools

import trry

class DeleteComment(Handler):
	
	@trry.user_logged_in
	@trry.comment_exist
	@trry.user_owns_comment
	def get(self, blog_id, comment):
		comment.delete()
		self.redirect('/blog/%s' % str(blog_id))