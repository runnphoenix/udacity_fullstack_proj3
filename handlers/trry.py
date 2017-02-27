#!/usr/bin/python

import functools
from google.appengine.ext import db

def blogs_key(name="default"):
	return db.Key.from_path("blogs", name)

def user_logged_in(function):
	@functools.wraps(function)
	def wrapper(self, *a):
		if self.user:
			return function(self, *a)
		else:
			print("------ user nog logged in.")
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
			print("------ blog post not exist.")
			self.error(404)
			return
	return wrapper