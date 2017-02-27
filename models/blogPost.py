#!/usr/bin/python

from google.appengine.ext import db
from user import User

class BlogPost(db.Model):
	title = db.StringProperty(required=True)
	content = db.TextProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)
	modified = db.DateTimeProperty(auto_now=True)

	def prepare_render(self):
		self.content = self.content.replace('\n', '<br>')
		
	user = db.ReferenceProperty(User, collection_name = "blog_posts")
		