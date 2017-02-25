#!/usr/bin/python

from handler import Handler
from models import Comment
from google.appengine.ext import db


def blogs_key(name="default"):
	return db.Key.from_path("blogs", name)

class DeleteComment(Handler):
	
	def get(self, blog_id, comment_id):
		comment_key = db.Key.from_path("Comment", int(comment_id))
		comment = db.get(comment_key)
		comment.delete()
		self.redirect('/blog/%s' % str(blog_id))