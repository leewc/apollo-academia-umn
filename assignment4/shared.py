UPLOAD_DIR = "pictures"
THUMBNAIL_SIZE = (140, 140)

def getTitle(path):
    with open(path, 'r') as file:
        return file.read()


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

# Takes a url to redirect to
REDIRECT_TEMPLATE = """
Location: %(URL)s \n\n
<!DOCTYPE html>"
<html>"
<head> </head>"
<body> </body>"
</html>"""
