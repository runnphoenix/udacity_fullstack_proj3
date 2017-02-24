#!/usr/bin/python

class Welcome(Handler):

	def get(self):
		if self.user:
			self.render("welcome.html", username=self.user.name)
		else:
			self.redirect('/login')