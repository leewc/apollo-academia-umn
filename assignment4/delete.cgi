#!/usr/bin/python

import cgi
import os
import glob
from shared import *  # import common templates and variables


form = cgi.FieldStorage()
fileid = form.getvalue("id")
title = ""
msg = ""
success = False


if os.environ['REQUEST_METHOD'] == 'GET':
    if fileid is not None:
        try:
            filePath = os.path.join(UPLOAD_DIR, fileid + ".txt")
            title = getTitle(filePath)
        except Exception as e:
            # msg = """<div id="message"> Invalid Image Title Requested, try another ID </div>"""
            msg = """<div id="message"> Please return to the Gallery to select a VALID image for deletion. </div>"""
    else:
        msg = """<div id="message"> Please return to the Gallery to select an image for deletion. </div>"""
else:  # delete the files!
    filePath = os.path.join(UPLOAD_DIR, fileid + ".jpg")
    if os.path.isfile(filePath):
        try:
            # os.remove(filePath)
            # os.remove(os.path.join(UPLOAD_DIR, fileid + "_tn.jpg"))
            # os.remove(os.path.join(UPLOAD_DIR, fileid + ".txt"))
            for fileName in glob.glob(os.path.join(UPLOAD_DIR, fileid + "*")): # much cleaner
                os.remove(fileName)
            success = True # writing true wasted my half an hour, tired.
            msg = "NOT NONE"
        except Exception as e:
            msg = """<div id="message"> Something went wrong, could not delete image. Please try again. """
    else:
        msg = """<div id="message"> Something went wrong, or image has already been deleted. Please try another. """


deleteForm = """
<form name="deleteForm" action="delete.cgi" method="POST" enctype="multipart/form-data">
%(msg)s 
Are you sure? You want to delete picture [ %(title)s ]. <br/>
<input name="id" type="hidden" value="%(fileid)s"/>
<button name="submit" type="submit"> Yes </button>
<a href="gallery.cgi"> <button type="button">Cancel</button></a>
</form>
""" % { 'title' : title, 'msg': msg, 'fileid': fileid }


strings = {
    'windowTitle': "Delete Photo",
    'title': "Delete Picture",
    'body': deleteForm
}

if os.environ['REQUEST_METHOD'] == 'GET':
    if msg != "":
        strings['body'] = msg
    print 'content-type: text/html\n'
    print HTML_TEMPLATE % strings

# Only true here if we post and fail the top conditons. Else redirected.
if not success and os.environ['REQUEST_METHOD'] == 'POST':
    strings['body'] = msg
    print 'content-type: text/html\n'
    print HTML_TEMPLATE % strings

if success and os.environ['REQUEST_METHOD'] == 'POST':
    REDIRECT('gallery.cgi')
