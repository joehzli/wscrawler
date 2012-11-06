from BeautifulSoup import BeautifulSoup
from BeautifulSoup import Tag
import HTMLParser
import re
import wsdb

GSID = ""

def ParseFollow(theContent):
    followSectionStart = '<script>STK && STK.pageletM && STK.pageletM.view({"pid":"pl_relation_hisFollow"'
    html_parser = HTMLParser.HTMLParser()
    urls = list()
    lines = theContent.splitlines()
    followContent = ""
    for line in lines:
        if line.startswith(followSectionStart):
            n = line.find('"html":"')
            if n > 0:
                followContent = line[n + 8: -12].decode("string_escape").replace("\\", "")
                break
    if followContent != "":
        soup = BeautifulSoup(followContent)
        #grab the urls of followings' in current page
        followings = soup.findAll('a',usercard=re.compile('id=*'))
        for user in followings:
            uid = user['usercard'][3:].encode("utf-8")
            urls.append({"type":"info", "url":"http://www.weibo.com/"+uid+"/info", "fetched":False})
            urls.append({"type":"follow", "url":"http://www.weibo.com/"+uid+"/follow", "fetched":False})
            urls.append({"type":"weibo", "url":"http://weibo.cn/"+uid+"/profile"+GSID, "fetched":False})

        #grab the urls of follow pages
        pageNode = soup.findAll(attrs={"class":"W_pages W_pages_comment"})
        if len(pageNode)>0 and pageNode[0] is not None:
            maxFollowPage = 1
            pages = list()
            for item in pageNode[0].contents:
                if item.string is not None and item.string.isdigit():
                    maxFollowPage = max(maxFollowPage, int(item.string))
                    if isinstance(item, Tag) and item.has_key("href"):
                        pages.append(item['href'])
            if len(pages) > 0:
                baseUrl = pages[0][:-1]
                for i in range(2,maxFollowPage+1):
                    urls.append({"type":"follow", "url":"http://www.weibo.com"+baseUrl.encode("utf-8")+str(i), "fetched":False})
        soup.decompose()
        db = wsdb.db
        for item in urls:
            if db.urlset.find({'url':item['url']}).count() < 1:
                db.urlset.insert(item)

def ParseInfo(theContent):
    #TBD
    return

def ParseWeibo(theContent):
    #TBD
    return