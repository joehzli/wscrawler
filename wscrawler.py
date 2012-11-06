import wsdb
import parsewb
import urllib
import urllib2
import time
import parsewb
import threading
import zlib

# select a downloader from this pool
downloaders = ["http://localhost:6543"],
                "http://localhost:6544",
                "http://localhost:6545"]

def FetchUrl():
    index = 0
    poolsize = len(downloaders)
    while True:
        urls = list(wsdb.db.urlset.find({'fetched':False}).limit(10))
        if len(urls) < 1:
            print "All urls have been fetched."
            time.sleep(3)
            continue
        for item in urls:
            downloaderHost = downloaders[index%poolsize]
            index=index+1
            param = {'url':item['url'], 'type':item['type']}
            url = downloaderHost + "/get?" + urllib.urlencode(param)
            try:
                response = urllib2.urlopen(url)
                print "Fetched %s:"%item['url'], response.read()
                response.close()
            except Exception, e:
                import traceback
                print "Exception occurs while getting %s"%item['url']
                print e
                print traceback.print_exc()

def ParseContent():
    while True:
        pages = list(wsdb.db.download.find({'parsed':False,'type':'follow'}).limit(10))
        if len(pages) < 1:
            print "All pages have been parsed."
            time.sleep(3)
            continue
        for page in pages:
            try:
                parsewb.ParseFollow(zlib.decompress(page['content']))
                wsdb.db.download.update({'_id':page['_id']},{'$set':{'parsed':True}})
                print "Parsed %s."%page['url']
            except Exception, e:
                import traceback
                print "Exception occurs while parsing %s"%page['url']
                print e
                print traceback.print_exc()

def main():
    fetchThread = threading.Thread(target=FetchUrl)
    parseThread = threading.Thread(target=ParseContent)
    fetchThread.start()
    parseThread.start()

if __name__ == "__main__":
    main()
