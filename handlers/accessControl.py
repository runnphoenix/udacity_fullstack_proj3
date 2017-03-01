#!/usr/bin/python

import functools
from google.appengine.ext import db


def blogs_key(name="default"):
    return db.Key.from_path("blogs", name)


def user_logged_in(function):
    @functools.wraps(function)
    def wrapper(self, *a):
        if self.user:
            return function(self, *a)
        else:
            print("------ user not logged in.")
            self.redirect('/login')
            return
    return wrapper


def post_exist(function):
    @functools.wraps(function)
    def wrapper(self, blog_id):
        key = db.Key.from_path("BlogPost", int(blog_id), parent=blogs_key())
        blog = db.get(key)
        if blog:
            return function(self, blog_id, blog)
        else:
            print("------ blog post not exist.")
            self.error(404)
            return
    return wrapper


def user_owns_blog(function):
    @functools.wraps(function)
    def wrapper(self, blog_id, blog):
        if self.user.name == blog.user.name:
            return function(self, blog_id, blog)
        else:
            print("------- user doesn't own blog")
            self.redirect('/blog/%s' % str(blog_id))
            return
    return wrapper


def comment_exist(function):
    @functools.wraps(function)
    def wrapper(self, blog_id, comment_id):
        comment_key = db.Key.from_path("Comment", int(comment_id))
        comment = db.get(comment_key)
        if comment:
            return function(self, blog_id, comment)
        else:
            print("------- comment doesn't exist.")
            self.error(404)
            return
    return wrapper


def user_owns_comment(function):
    @functools.wraps(function)
    def wrapper(self, blog_id, comment):
        if self.user.name == comment.author:
            return function(self, blog_id, comment)
        else:
            print("------- user doesn't own comment.")
            self.redirect('/blog/%s' % str(blog_id))
            return
    return wrapper
