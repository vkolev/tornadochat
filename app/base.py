import tornado.web
from app.chattr import ChatSocketHandler

class MainHandler(tornado.web.RequestHandler):

    def get(self):
	if not self.get_secure_cookie("username"):
	    self.redirect("/login")
	    return
	else:
	    user = self.get_secure_cookie("username");
	    self.render("index.html", messages=ChatSocketHandler.cache, user=user)
