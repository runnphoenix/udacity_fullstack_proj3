#!/usr/bin/python

from handler import Handler
from google.appengine.ext import db
import functools

def blogs_key(name="default"):
	return db.Key.from_path("blogs", name)
	
class EditBlog(Handler):
	def post_exist(function):
		@functools.wraps(function)
		def wrapper(self, blog_id):
			key = db.Key.from_path("BlogPost", int(blog_id), parent=blogs_key())
			blog = db.get(key)
			if blog:
				return function(self, blog_id, blog)
			else:
				self.error(404)
				return
		return wrapper
		
	def user_logged_in(function):
		@functools.wraps(function)
		def wrapper(self, *a):
			if self.user:
				return function(self, *a)
			else:
				self.redirect('/login')
				return
		return wrapper
		
	def user_owns_blog(function):
		@functools.wraps(function)
		def wrapper(self, blog_id, blog):
			if self.user.name == blog.user.name:
				return function(self, blog_id, blog)
			else:
				self.redirect('/blog/%s' % str(blog_id))
				return
		return wrapper
	
	
	@user_logged_in
	@post_exist
	@user_owns_blog
	def get(self, blog_id, blog):
		self.render("editBlog.html", blog=blog)
	
	@user_logged_in
	@post_exist
	@user_owns_blog
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
