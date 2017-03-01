#!/usr/bin/python

from handler import Handler
import accessControl


class DeleteComment(Handler):

    @accessControl.user_logged_in
    @accessControl.comment_exist
    @accessControl.user_owns_comment
    def get(self, blog_id, comment):
        comment.delete()
        self.redirect('/blog/%s' % str(blog_id))
