#!/usr/bin/python
from google.appengine.ext import db

class BlogPost(db.Model):
	title = db.StringProperty(required=True)
	content = db.TextProperty(required=True)
	author = db.StringProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)
	modified = db.DateTimeProperty(auto_now=True)

	def prepare_render(self):
		self.content = self.content.replace('\n', '<br>')
		