#!/usr/bin/python
from google.appengine.ext import db

class Like(db.Model):
	blog_id = db.IntegerProperty(required=True)
	fromed = db.StringProperty(required=True)