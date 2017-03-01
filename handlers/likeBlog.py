#!/usr/bin/python

from handler import Handler
from models import Like
from google.appengine.ext import db
import accessControl


def blogs_key(name="default"):
    return db.Key.from_path("blogs", name)


class LikeBlog(Handler):

    @accessControl.user_logged_in
    @accessControl.post_exist
    def get(self, blog_id, blog):
        toAdd = True
        like = Like(blog_post=blog, fromed=self.user.name)
        for liked in blog.likes:
            if liked.fromed == like.fromed:
                toAdd = False
        if toAdd:
            like.put()

        self.redirect('/blog/%s' % str(blog_id))
