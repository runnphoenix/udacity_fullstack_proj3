#!/usr/bin/python

from handler import Handler
from models import Comment
import accessControl


class BlogPage(Handler):

    @accessControl.user_logged_in
    @accessControl.post_exist
    def get(self, blog_id, blog):
        blog.prepare_render()

        is_author = (self.user.name == blog.user.name)

        liked = False
        likes_count = 0
        for like in blog.likes:
            likes_count = likes_count + 1
            if like.fromed == self.user.name:
                liked = True

        self.render(
            "blogPost.html",
            blog=blog,
            is_author=is_author,
            userName=self.user.name,
            likes_count=likes_count,
            liked=liked)

    @accessControl.user_logged_in
    @accessControl.post_exist
    def post(self, blog_id, blog):
        # Comment
        commentContent = self.request.get('commentContent')
        if commentContent:
            newcomment = Comment(
                blog_post=blog,
                content=commentContent,
                author=self.user.name)
            newcomment.put()
        self.redirect('/blog/%s' % str(blog_id))
