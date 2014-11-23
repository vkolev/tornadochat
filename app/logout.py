import tornado.web

class LogoutHandler(tornado.web.RequestHandler):

    def get(self):
	self.clear_all_cookies()
	self.redirect("/")
