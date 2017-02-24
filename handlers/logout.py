#!/usr/bin/python

class Logout(Handler):

    def get(self):
	self.reset_cookie()
	self.redirect('/login')
