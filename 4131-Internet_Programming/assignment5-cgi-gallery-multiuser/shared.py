import Cookie
import os 

UPLOAD_DIR = "pictures"
THUMBNAIL_SIZE = (140, 140)

def getTitle(path):
    with open(path, 'r') as file:
        return file.read()

# Returns a boolean on whether the user is already logged in, done by checking cookies
def isLoggedIn():
    cookie_str = os.environ.get('HTTP_COOKIE')
    if not cookie_str:
        return False
    cookie = Cookie.SimpleCookie()
    cookie.load(cookie_str)
    if cookie.get('login') is None:
        return False
    return cookie['login'].value == 'True'

"""
HTML_TEMPLATE requires a dictionary that must have the following key-values
{
    'windowTitle':
    'title':
    'body':
}
"""
HTML_TEMPLATE = """
<!DOCTYPE html">
<html>
<head>
    <title>%(windowTitle)s</title>
    <meta http-equiv="Content-Type" content="text/html; charset="utf-8""/>
    <link rel="stylesheet" href="style.css" />
</head>
<body>
    <h1>%(title)s</h1>
    <!-- body text-->
    %(body)s
</body>
</html>"""

# Takes a url to redirect to, template didn't work.
def REDIRECT(url):
    print "Content-Type: text/html"
    print "Location:" + url
    print
    print "<!DOCTYPE html>"
    print "<html>"
    print "<head> </head>"
    print "<body> </body>"
    print "</html>"

