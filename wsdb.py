from pymongo import Connection

db = None
connection = None
username = ""
password = ""

def initDB():
    global connection
    connection = Connection('localhost',27017)
    global db
    db = connection.admin
    db.authenticate(username,password)
    db = connection.wscrawler

initDB()