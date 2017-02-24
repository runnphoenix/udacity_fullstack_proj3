#!/usr/bin/python

class BlogPage(Handler):

	def get(self, blog_id):
		key = db.Key.from_path("Blog", int(blog_id), parent=blogs_key())
		blog = db.get(key)

		if not blog:
			self.error(404)
			return

		blog.prepare_render()

		is_author = False
		if self.user:
			is_author = (self.user.name == blog.author)

		comments = db.GqlQuery(
			"select * from Comment where blog_id = :1 order by created", key.id())
		likes = db.GqlQuery("select * from Like where blog_id = :1", key.id())
		likeCount = 0
		liked = False
		for like in likes:
			likeCount = likeCount + 1
			if like.fromed == self.user.name:
				liked = True
			
		self.render(
			"blogPost.html",
			blog=blog,
			is_author=is_author,
			userName=self.user.name,
			comments=comments,
			likes=likes,
			likeCount=likeCount,
			liked=liked)

	def post(self, blog_id):
		key = db.Key.from_path("Blog", int(blog_id), parent=blogs_key())
		blog = db.get(key)
		comment_id = self.request.get("comment")
		if comment_id:
			comment_key = db.Key.from_path("Comment", int(comment_id))
			comment = db.get(comment_key)

		commentContent = self.request.get("commentContent")
		params = self.request.params
		# Edit
		if "editButton" in params:
			self.redirect('/blog/edit/%s' % str(blog.key().id()))
		# Like
		elif "likeButton" in params:
			toAdd = True
			like = Like(fromed=self.user.name, blog_id=key.id())
			likes = db.GqlQuery(
				"select * from Like where blog_id = :1", key.id())
			for liked in likes:
				if liked.fromed == like.fromed:
					toAdd = False
			if toAdd:
				like.put()
			self.redirect('/blog/%s' % str(blog_id))
		# Delete
		elif "deleteButton" in params:
			blog.delete()
			self.redirect("/blog/?")
		# Delete Comment
		elif "deleteComment" in params:
			comment.delete()
			self.redirect('/blog/%s' % str(blog_id))
		# Edit Comment
		elif "editComment" in params:
			self.redirect(
				'/blog/%s/%s' %
				(str(
					blog.key().id()), str(
					comment.key().id())))
		# Comment
		elif commentContent:
			newcomment = Comment(
				content=commentContent,
				author=self.user.name,
				blog_id=key.id())
			newcomment.put()
			self.redirect('/blog/%s' % str(blog_id))
		else:
			self.redirect('/blog/%s' % str(blog_id))