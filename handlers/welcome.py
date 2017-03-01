#!/usr/bin/python

from handler import Handler
import accessControl


class Welcome(Handler):

    @accessControl.user_logged_in
    def get(self):
        self.render("welcome.html", username=self.user.name)
