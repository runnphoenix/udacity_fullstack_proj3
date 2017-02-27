#!/usr/bin/python

from handler import Handler
from models import Comment
from google.appengine.ext import db
import functools

import trry

class EditComment(Handler):
	
	@trry.user_logged_in
	@trry.comment_exist
	@trry.user_owns_comment
	def get(self, blog_id, comment):
		self.render("editComment.html", blog_id=blog_id, comment=comment)
	
	@trry.user_logged_in
	@trry.comment_exist
	@trry.user_owns_comment
	def post(self, blog_id, comment):
		newCommentContent = self.request.get("content")
		comment.content = newCommentContent
		comment.put()
		self.redirect("/blog/%s" % blog_id)
