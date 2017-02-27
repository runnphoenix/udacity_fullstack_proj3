#!/usr/bin/python

from handler import Handler
from google.appengine.ext import db
import functools

import trry
	
class EditBlog(Handler):
		
	@trry.user_logged_in
	@trry.post_exist
	@trry.user_owns_blog
	def get(self, blog_id, blog):
		self.render("editBlog.html", blog=blog)
	
	@trry.user_logged_in
	@trry.post_exist
	@trry.user_owns_blog
	def post(self, blog_id, blog):
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
			blog.title = blogTitle
			blog.content = blogContent
			blog.put()
			# goto blog page
			self.redirect("/blog/%s" % str(blog.key().id()))

	def erMessage(self, blogTitle, blogContent):
		if blogTitle and (not blogContent):
			return "Content is empty"
		elif (not blogTitle) and blogContent:
			return "Title is empty"
		elif (not blogTitle) and (not blogContent):
			return "Both title and content empty"
		else:
			return None
