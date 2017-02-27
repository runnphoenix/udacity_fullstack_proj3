#!/usr/bin/python

from handler import Handler
from models import Comment
from models import Like

from google.appengine.ext import db
import functools

def blogs_key(name="default"):
	return db.Key.from_path("blogs", name)

class BlogPage(Handler):
	def user_logged_in(function):
		@functools.wraps(function)
		def wrapper(self, *a):
			if self.user:
				return function(self, *a)
			else:
				self.redirect('/login')
				return
		return wrapper
			
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
	
	@user_logged_in		
	@post_exist
	def get(self, blog_id, blog):
		blog.prepare_render()

		is_author = (self.user.name == blog.user.name)
		
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
	
	@user_logged_in
	@post_exist
	def post(self, blog_id, blog):
		# Comment
		commentContent = self.request.get('commentContent')
		if commentContent:
			newcomment = Comment(
				blog_post = blog,
				content=commentContent,
				author=self.user.name)
			newcomment.put()
		self.redirect('/blog/%s' % str(blog_id))
			