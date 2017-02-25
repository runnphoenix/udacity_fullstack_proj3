#!/usr/bin/python

from google.appengine.ext import db
from comment import Comment

class BlogPost(db.Model):
	title = db.StringProperty(required=True)
	content = db.TextProperty(required=True)
	author = db.StringProperty(required=True)
	created = db.DateTimeProperty(auto_now_add=True)
	modified = db.DateTimeProperty(auto_now=True)

	def prepare_render(self):
		self.content = self.content.replace('\n', '<br>')
		
	@property
	def comments(self):
		#return comments in this function
		comments = db.GqlQuery(
		"select * from Comment where blog_id = :1 order by created", self.key().id())
		return comments
	
	@property 
	def likes(self):
		likes = db.GqlQuery("select * from Like where blog_id = :1", self.key().id())
		return likes
		