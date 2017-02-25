#!/usr/bin/python

from handler import Handler
from models import Comment
from models import Like

from google.appengine.ext import db

def blogs_key(name="default"):
	return db.Key.from_path("blogs", name)

class BlogPage(Handler):

	def get(self, blog_id):
		blog_key = db.Key.from_path("BlogPost", int(blog_id), parent=blogs_key())
		blog = db.get(blog_key)

		if not blog:
			self.error(404)
			return

		blog.prepare_render()

		is_author = False
		if self.user:
			is_author = (self.user.name == blog.author)
		
		liked = False
		likes_count = 0
		for like in blog.likes:
			likes_count = likes_count + 1
			if like.fromed == self.user.name:
				liked = True
		
		self.render(
			"blogPost.html",
			blog=blog,
			is_author=is_author,
			userName=self.user.name,
			likes_count=likes_count,
			liked=liked)

	def post(self, blog_id):
		key = db.Key.from_path("BlogPost", int(blog_id), parent=blogs_key())
		blog = db.get(key)
		comment_id = self.request.get("comment")
		if comment_id:
			comment_key = db.Key.from_path("Comment", int(comment_id))
			comment = db.get(comment_key)

		commentContent = self.request.get("commentContent")
		params = self.request.params
			
		# Comment
		if commentContent:
			newcomment = Comment(
				content=commentContent,
				author=self.user.name,
				blog_id=key.id())
			newcomment.put()
			self.redirect('/blog/%s' % str(blog_id))
		else:
			self.redirect('/blog/%s' % str(blog_id))
			