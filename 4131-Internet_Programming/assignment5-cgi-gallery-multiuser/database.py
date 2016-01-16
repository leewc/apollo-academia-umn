import os
import Cookie
import ConfigParser
import MySQLdb

class Database:
    def __init__(self):
        self.db = None # global variable that will hold the database reference
        self.host = None # str
        self.port = None # int
        self.user = None # str
        self.passwd = None #str
        self.db_name = None #str
        self.cookie_expiration = None # int
        
        self.readConfigFile('config') # populates the database class
        self.connectAndSelectDB() # establish a connection to the DB, and select table

    def readConfigFile(self,filename):
        # read information from config file using the ConfigParser, built in Python
        Config = ConfigParser.ConfigParser()
        Config.read(filename)
        self.host = Config.get('Database', 'host')
        self.port = Config.getint('Database', 'port')
        self.user = Config.get('Database', 'user')
        self.passwd = Config.get('Database', 'passwd')
        self.db_name = Config.get('Database', 'db_name')
        self.cookie_expiration = Config.getint('Database','cookie_expiration')

    # establish connection and select table
    def connectAndSelectDB(self):
        self.db = MySQLdb.connect(host=self.host, user=self.user, 
                             passwd=self.passwd, port=self.port)
        self.db.select_db(self.db_name)
        return True

    def runQuery(self, query, args):
        """Each Row is checked to be unique before insertion,
        even if adding return at most one so fetchone only.
        args must be a tuple, that holds the string formats.
        avoids SQL injection. (Previous Version did not have this)
        http://bobby-tables.com/python.html
        """
        cursor = self.db.cursor()
        try:
            cursor.execute(query, args)
        except:
            db.rollback()
        result = cursor.fetchone()
        cursor.close()
        return result
        
    # helper to determine if user is owner
    def isOwner(self, username):
        result = self.runQuery("SELECT Role FROM Users WHERE Name=%s", username)
        return 'Owner' in result

    # helper to determine if user exists in the db before update,change,delete
    def exists(self, username):
        exists = self.runQuery("SELECT * FROM Users "
                               "WHERE Name=%s", username)
        return True if exists is not None else False

    # checks if credentials match
    def login(self, username, password):
        """Since username is unique before adding into the DB 
        we don't have to check for it here."""
        result = self.runQuery(("SELECT * FROM Users "
                                "WHERE Name=%s AND Password=%s"),
                               (username, password))
	if result is None:
	   return False
        return True

    # adds a user to the DB, only visitors
    def addUser(self, username, password):
        """Only have new visitor roles, no more Owners."""
        if self.exists(username):
            return False

        result = self.runQuery("INSERT INTO Users "
                               "(Name, Role, Password) "
                               "VALUES (%s, 'Visitor',%s)",
                               (username, password))
        self.db.commit() # else changes might not be commited
        if result is not None:
            return False # failed
        return True # success

    # updates a user's password with a new password
    def changePassword(self, username, password):
        if not self.exists(username):
            return False
        
        result = self.runQuery("UPDATE Users " 
                               "SET Password=%s "
                               "WHERE Name=%s LIMIT 1",
                               (password, username))
        self.db.commit() # else changes might not be commited
        if result is not None:
            return False # failed
        return True # success

    # deletes a user if username exists and is not owner
    def deleteUser(self,username):
        if not self.exists(username):
            return False

        if self.isOwner(username): 
            # could also have done it in one Query but this is more explicit
            return False
        result = self.runQuery("DELETE FROM Users WHERE Name=%s LIMIT 1",(username))
        self.db.commit()

        if result is not None:
            return False # failed
        return True # success
    
    # makes a cookie that expires based on time set in config file
    def makeCookie(self, username):
        cookie = Cookie.SimpleCookie()
        cookie['username'] = username
        cookie['login'] = True
        for key, morsel in cookie.iteritems():
            morsel['max-age'] = self.cookie_expiration
        print cookie # this is how you actually 'save' it LOL 
        # Credit: http://raspberrywebserver.com/cgiscripting/using-python-to-set-retreive-and-clear-cookies.html
        return True

    # reads a cookie and checks if user is owner
    def isOwnerFromCookie(self):
        cookie = Cookie.SimpleCookie()
        cookie_str = os.environ.get('HTTP_COOKIE')
        if not cookie_str:
            return False
        cookie = Cookie.SimpleCookie()
        cookie.load(cookie_str)
        if cookie.get('username') is None:
            return False
        return self.isOwner(cookie['username'].value)

