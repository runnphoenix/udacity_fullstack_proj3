#!/usr/bin/python

from handler import Handler
import functools

class Welcome(Handler):
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
		self.render("welcome.html", username=self.user.name)