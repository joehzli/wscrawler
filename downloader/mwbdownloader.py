import urllib
import urllib2
import cookielib
import base64
import re
import json
import hashlib
import wsdb
import datetime
import zlib
from bson.binary import Binary

cj = cookielib.LWPCookieJar()
cookie_support = urllib2.HTTPCookieProcessor(cj)
opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
urllib2.install_opener(opener)

def download(theUrl, theType):
    headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0'}
    req  = urllib2.Request(
        url = theUrl,
        headers = headers
    )
    result = urllib2.urlopen(req)
    text = result.read()
    entity = dict()
    entity["url"] = theUrl
    entity["type"] = theType
    entity["content"] = Binary(zlib.compress(text))
    entity["parsed"] = False
    entity["time"] = datetime.datetime.now()
    wsdb.db.download.insert(entity)
    wsdb.db.urlset.update({'url':theUrl},{'$set':{'fetched':True}})