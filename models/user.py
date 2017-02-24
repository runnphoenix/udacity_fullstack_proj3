#!/usr/bin/python
from google.appengine.ext import db

def users_key(group='default'):
	return db.Key.from_path("users", group)

def make_salt(length=5):
	return ''.join(random.choice(letters) for x in xrange(length))

def make_pw_hash(name, pw, salt=None):
	if not salt:
		salt = make_salt()
	h = hashlib.sha256(name + pw + salt).hexdigest()
	return "%s,%s" % (salt, h)

def valid_hash(name, pw, h):
	salt = h.split(',')[0]
	return h == make_pw_hash(name, pw, salt)

class User(db.Model):
	name = db.StringProperty(required=True)
	pw_hash = db.StringProperty(required=True)
	email = db.StringProperty()

	@classmethod
	def by_name(cls, name):
		u = User.all().filter('name =', name).get()
		return u

	@classmethod
	def by_id(cls, user_id):
		return User.get_by_id(user_id, parent=users_key())

	@classmethod
	def signup(cls, username, pw, email=None):
		pw_hash = make_pw_hash(username, pw)
		user = User(name=username, pw_hash=pw_hash, email=email)