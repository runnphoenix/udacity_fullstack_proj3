#!/usr/bin/python

from handler import Handler
from google.appengine.ext import db

def blogs_key(name="default"):
	return db.Key.from_path("blogs", name)

class EditComment(Handler):

	def get(self, blog_id, comment_id):
		blog_key = db.Key.from_path("BlogPost", int(blog_id), parent=blogs_key())
		blog = db.get(blog_key)
		comment_key = db.Key.from_path("Comment", int(comment_id))
		comment = db.get(comment_key)
		self.render("editComment.html", blog=blog, comment=comment)

	def post(self, blog_id, comment_id):
		newCommentContent = self.request.get("content")
		comment_key = db.Key.from_path("Comment", int(comment_id))
		comment = db.get(comment_key)
		comment.content = newCommentContent
		comment.put()
		self.redirect("/blog/%s" % blog_id)
