import mwbdownloader
import wbdownloader
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.httpserver
import tornado.autoreload
import threading
from tornado.options import define, options

MAXTHREAD = 20
sema = threading.BoundedSemaphore(MAXTHREAD)

define("port", default=6543, help="run on the given port", type=int)

class DownloaderHandler(tornado.web.RequestHandler):
    def get(self):
        global sema
        url = self.get_argument('url')
        t = self.get_argument('type')
        if url is None or t is None:
            return
        self.write("received")
        self.finish()
        sema.acquire()
        threading.Thread(target = download, args=(url, t,)).start()
        

def download(theUrl, theType):
    try:
        if theType == "weibo":
            mwbdownloader.download(theUrl, theType)
        if theType == "info" or theType == "follow":
            wbdownloader.download(theUrl, theType)
    except Exception, e:
        import traceback
        print "Exception occurs while parsing %s"%theUrl
        print e
        print traceback.print_exc()
    finally:
        global sema
        sema.release()

def main():
    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/get", DownloaderHandler),
        ])
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
    

