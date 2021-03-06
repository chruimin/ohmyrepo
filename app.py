# coding: UTF-8
import tornado.auth
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.autoreload
from tornado.options import define, options
from handlers import *
import session
from settings import settings
from cache import RedisCacheBackend
import redis

define("port", default=8888, help="run on the given port", type=int)
define("debug", default=True, help="debug mode", type=bool)
define("mongo_host", default="127.0.0.1:27017", help="database host")
define("mongo_database", default="quora", help="database name")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", HomeHandler),
            (r"/logout", LogoutHandler),
            (r"/webhook", WebhookHandler),
            (r"/callback", CallbackHandler),
            (r"/stars", UserStarHandler),
            (r"/follows", UserFollowingHandler),
            (r"/cities", UserCityhandler),
            (r"/f", FollowHandler),
            (r"/uf", UnfollowHandler),
            (r"/add", AddWebhookHandler),
            (r"/show", ShowHandler),
            (r"/login", LoginHandler),
            (r"/howitwork", HowHandler)
        ]
        self.session_manager = session.TornadoSessionManager(settings["session_secret"], settings["session_dir"])
        self.redis = redis.Redis()
        self.cache = RedisCacheBackend(self.redis)
        debug = False
        tornado.web.Application.__init__(self, handlers, **settings)


def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    instance = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(instance)
    instance.start()

if __name__ == "__main__":
    main()
