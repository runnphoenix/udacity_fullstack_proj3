#!/usr/bin/python
from google.appengine.ext import db
from blogPost import BlogPost

class Like(db.Model):
	fromed = db.StringProperty(required=True)
	
	blog_post = db.ReferenceProperty(BlogPost, collection_name = "likes")