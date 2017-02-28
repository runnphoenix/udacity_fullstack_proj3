#!/usr/bin/python

from handler import Handler
from models import Comment
from google.appengine.ext import db
import functools

import accessControl

class EditComment(Handler):
	
	@accessControl.user_owns_comment
	@accessControl.comment_exist
	@accessControl.user_logged_in
	def get(self, blog_id, comment):
		self.render("editComment.html", blog_id=blog_id, comment=comment)
		
	@accessControl.user_owns_comment
	@accessControl.comment_exist
	@accessControl.user_logged_in
	def post(self, blog_id, comment):
		newCommentContent = self.request.get("content")
		comment.content = newCommentContent
		comment.put()
		self.redirect("/blog/%s" % blog_id)
