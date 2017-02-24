#!/usr/bin/python

class NewPost(Handler):

	def get(self):
		if self.user:
			self.render("newpost.html")
		else:
			self.redirect("/login")

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
			blog = Blog(
				parent=blogs_key(),
				title=blogTitle,
				content=blogContent,
				author=self.user.name)
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