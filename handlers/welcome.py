#!/usr/bin/python

from handler import Handler

class Welcome(Handler):

	def get(self):
		if self.user:
			self.render("welcome.html", username=self.user.name)
		else:
			self.redirect('/login')