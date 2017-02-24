#!/usr/bin/python

class Blogs(Handler):

	def get(self):
		# Show blogs
		blogs = db.GqlQuery(
			"select * from Blog order by created desc limit 10")
		self.render("blogs.html", blogs=blogs)
