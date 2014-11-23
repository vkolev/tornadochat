import tornado.web

class LoginHandler(tornado.web.RequestHandler):

    def get(self):
	if not self.get_secure_cookie("username"):
	    self.render("login.html")
	else:
	    self.redirect("/")

    def post(self):
	self.set_secure_cookie("username", self.get_argument("username"))
	self.redirect("/")
