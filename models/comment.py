#!/usr/bin/python
from google.appengine.ext import db

class Comment(db.Model):
	content = db.TextProperty(required=True)
	author = db.StringProperty(required=True)
	blog_id = db.IntegerProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)
	modified = db.DateTimeProperty(auto_now=True)
