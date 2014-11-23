import logging
import uuid
import hashlib
import tornado.escape
import tornado.websocket

class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    cache = []
    cache_size = 200

    def get_sompression_options(self):
        return {}

    def open(self):
	ChatSocketHandler.waiters.add(self)

    def on_close(self):
	ChatSocketHandler.waiters.remove(self)

    @classmethod
    def update_cache(cls, chat):
	cls.cache.append(chat)
	if len(cls.cache) > cls.cache_size:
	    cls.cache = cls.cache[-cls.cache_size:]

    @classmethod
    def send_updates(cls, chat):
	logging.info("sending message to %d waiters", len(cls.waiters))
	for waiter in cls.waiters:
	    try:
		waiter.write_message(chat)
	    except:
		logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
	logging.info("got message %r", message)
	parsed = tornado.escape.json_decode(message)
	username = str(self.get_secure_cookie("username"))
	chat = {
		"id": str(uuid.uuid4()),
		"username": username,
		"color": "#"+hashlib.md5(username).hexdigest()[:6],
		"body": parsed["body"],
		}
	chat["html"] = tornado.escape.to_basestring(
		self.render_string("message.html", message=chat))
	ChatSocketHandler.update_cache(chat)
	ChatSocketHandler.send_updates(chat)
