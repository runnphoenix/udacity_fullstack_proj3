#!/usr/bin/python
from google.appengine.ext import db
from blogPost import BlogPost


class Comment(db.Model):
    content = db.TextProperty(required=True)
    author = db.StringProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    modified = db.DateTimeProperty(auto_now=True)

    blog_post = db.ReferenceProperty(BlogPost, collection_name="comments")
