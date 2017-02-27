#!/usr/bin/python

from handler import Handler
from google.appengine.ext import db

class Blogs(Handler):

	def get(self):
		# Show blogs
		blogs = db.GqlQuery(
			"select * from BlogPost order by created desc")
		self.render("blogs.html", blogs=blogs)
