# import time
import tornado
from tornado.web import Application
from tornado.websocket import WebSocketHandler
from lib.net import get_remote_detail
from config import config


class websocketHandler(WebSocketHandler):

    def check_origin(self, origin):
        if config.SERVER_IP in origin:
            return True
        return False

    def on_message(self, message):
        self.ws_connection.close()

    def open(self):
        for item in get_remote_detail():
                json_data1 = item.json_format()
                self.write_message(json_data1.encode('utf-8'))


class MonitorApplication(Application):
    def __init__(self, *args, **kwargs):
        handler = [
            (r'/ws', websocketHandler)
        ]
        Application.__init__(self, handler)


if __name__ == "__main__":
    app = MonitorApplication()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(config.SERVER_PORT)
    loop = tornado.ioloop.IOLoop.instance()
    print("server staring...")
    try:
        loop.start()
    except KeyboardInterrupt:
        print("closing...")
        exit
