#!/usr/bin/python

from handler import Handler
from models import BlogPost
from google.appengine.ext import db
import functools

def blogs_key(name="default"):
	return db.Key.from_path("blogs", name)

class NewPost(Handler):
	def user_logged_in(function):
		@functools.wraps(function)
		def wrapper(self):
			if self.user:
				return function(self)
			else:
				self.redirect("/login")
				return
		return wrapper

	@user_logged_in
	def get(self):
		self.render("newpost.html")
	
	@user_logged_in
	def post(self):
		blogTitle = self.request.get("subject")
		blogContent = self.request.get("content")

		# Judge title and content
		errorMessage = self.erMessage(blogTitle, blogContent)
		if errorMessage:
			self.render(
				"newpost.html",
				errorMessage=errorMessage,
				blogTitle=blogTitle,
				blogContent=blogContent)
		else:
			# write db
			blog = BlogPost(
				user=self.user,
				parent=blogs_key(),
				title=blogTitle,
				content=blogContent)
			blog.put()
			# goto blog page
			self.redirect("/blog/%s" % str(blog.key().id()))

	def erMessage(self, blogTitle, blogContent):
		if blogTitle and (not blogContent):
			return "Content is empty."
		elif (not blogTitle) and blogContent:
			return "Title is empty."
		elif (not blogTitle) and (not blogContent):
			return "Both title and content empty."
		else:
			return None