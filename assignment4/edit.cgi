#!/usr/bin/python
import cgi
import os
from shared import *

form = cgi.FieldStorage()
fileid = form.getvalue("id")
newTitle = form.getvalue("title")
title = ""
msg = ""
success = False

if os.environ['REQUEST_METHOD'] == 'GET':
    if fileid is not None:
        try:
            filePath = os.path.join(UPLOAD_DIR, fileid + ".txt")
            title = getTitle(filePath)
        except Exception as e:
            msg = """<div id="message"> Invalid Image ID. Please return to the <a href="gallery.cgi">Gallery</a> to select and image.</div>"""
    else:
        msg = """<div id="message"> Please enter a valid title. </div>"""
else:
    newTitle = form.getvalue("title")
    if len(newTitle) > 0 and len(newTitle) < 100:
        with open(os.path.join(UPLOAD_DIR, fileid + ".txt"), "w") as file:
            file.write(newTitle)
        success = True
        print REDIRECT('gallery.cgi')
    else:
        msg = """<div id="message"> Please enter a valid title. </div>"""

editForm = """
<form name="editForm" action="edit.cgi" method="POST" enctype="multipart/form-data">
%(msg)s 
Title: <input name="title" type="text" value="%(prevTitle)s"></br>
<input name="id" type="hidden" value="%(fileid)s"/>
<button name="submit" type="submit">Update</button>
<a href="gallery.cgi"> <button type="button">Cancel</button></a>
</form>
""" % { 'prevTitle' : title, 'msg': msg, 'fileid': fileid }


strings = {
    'windowTitle': "Edit Photo Title",
    'title': "Edit Picture Title",
    'body': editForm
}

if os.environ['REQUEST_METHOD'] == 'GET':
    print 'content-type: text/html\n'
    print HTML_TEMPLATE % strings

# Only true here if we post and fail the top conditons. Else redirected.
if not success and os.environ['REQUEST_METHOD'] == 'POST':
    print 'content-type: text/html\n'
    print HTML_TEMPLATE % strings
