#!/usr/bin/python

# MainPage
class MainPage(Handler):

    def get(self):
	self.render("base.html")