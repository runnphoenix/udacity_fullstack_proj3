import webapp2
from google.appengine.ext import db

# imports Models
from models import User
from models import Like
from models import Comment
from models import BlogPost

#imports Handlers
from handlers import Signup
from handlers import Login
from handlers import BlogPage
from handlers import Blogs
from handlers import EditBlog
from handlers import EditComment
from handlers import Logout
from handlers import MainPage
from handlers import NewPost
from handlers import Welcome


app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/signup', Signup),
    ('/login', Login),
    ('/logout', Logout),
    ('/welcome', Welcome),
    ('/blog/?', Blogs),
    ('/blog/([0-9]+)', BlogPage),
    ('/blog/edit/([0-9]+)', EditBlog),
    ('/blog/([0-9]+)/([0-9]+)', EditComment),
    ('/blog/newpost', NewPost)
], debug=True)
