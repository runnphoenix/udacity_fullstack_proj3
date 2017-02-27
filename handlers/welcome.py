#!/usr/bin/python

from handler import Handler
import functools

import trry

class Welcome(Handler):
	
	@trry.user_logged_in	
	def get(self):
		self.render("welcome.html", username=self.user.name)