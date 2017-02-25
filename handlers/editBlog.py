#!/usr/bin/python

from handler import Handler
from google.appengine.ext import db

def blogs_key(name="default"):
	return db.Key.from_path("blogs", name)
	
class EditBlog(Handler):

	def get(self, blog_id):
		key = db.Key.from_path("BlogPost", int(blog_id), parent=blogs_key())
		blog = db.get(key)

		if not blog:
			self.error(404)
			return

		self.render("editBlog.html", blog=blog)

	def post(self, blog_id):
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
			key = db.Key.from_path("BlogPost", int(blog_id), parent=blogs_key())
			blog = db.get(key)
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
