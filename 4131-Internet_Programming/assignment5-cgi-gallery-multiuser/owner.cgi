#!/usr/bin/python
import cgi
import os

from shared import *
from database import *

import cgitb
cgitb.enable()

# Templates for the form and webpage
# make sure to put a string in for msg.
owner_form = """
<div id="buttons">
<a href="gallery.cgi"><button type=button> Go to Gallery </button></a>
<a href="upload.cgi"><button type=button> Upload a New Picture</button></a></div>
<b>%s</b>
<form name="addForm" action="owner.cgi" method="POST" enctype="multipart/form-data">
 <h2> Add a User </h2>
 Username: <input type='text' name='newUsername' />
 <br/>
 Password: <input type='password' name='password' />
 <br/>
<input type='submit' value='Add' name='addUser' />
</form>
<form name="deleteForm" action="owner.cgi" method="POST" enctype="multipart/form-data">
 <h2> Delete a User </h2>
 Username to Delete: <input type='text' name='deleteUsername' />
 <br/>
 <input type='submit' value='Delete' name='deleteUser'/>
</form>
<form name="changePasswordForm" action="owner.cgi" method="POST" enctype="multipart/form-data">
 <h2> Change User Password </h2>
 Username: <input type='text' name='changePwdUsername' />
 <br/>
 New Password: <input type='password' name='newPassword'/> 
 <br/>
 <input type='submit' value='Change' name='changePwd'/>
</form>
"""

strings = {
    'windowTitle': "Owner Menu",
    'title': "Welcome, Owner.",
    'body': owner_form % ""
}

# Set actions that can be performed by the Owner, interacts with a database connection instance
def ownerActions():
    db = Database()
    form = cgi.FieldStorage()
    msg = ""
    if 'addUser' in form:
        username = form['newUsername'].value
        password = form['password'].value
        if len(username) > 0 and len(password) > 0:
            if db.addUser(username, password):
                msg = """<div id="message"> New User successfully added.</div>"""
            else:
                msg = """<div id="message"> Error: Duplicate User or Something went wrong. </div>"""
        else:
            msg = """<div id="message"> Please enter a valid username and password.</div>"""
    
    elif 'deleteUser' in form:
        username = form['deleteUsername'].value
        if len(username) > 0:
            if db.deleteUser(username):
                msg = """<div id="message"> User Successfully Deleted </div>"""
            else:
                msg = """<div id="message"> Error: User not found or could not delete user. </div>"""
        else: 
            msg="""<div id="message"> Please enter a valid username for deletion. </div>"""
    elif 'changePwd' in form:
        username = form['changePwdUsername'].value
        newPassword = form['newPassword'].value
        if len(username) > 0 and len(newPassword) > 0:
            if db.changePassword(username, newPassword):
                msg = """<div id="message"> Password Successfully Updated.</div>"""
            else:
                msg = """<div id="message"> Error: Unable to change password. Either user does not exist or could not update password. </div>"""
        else:
            msg = """<div id="message"> Please enter a valid username and password to change.</div>"""        

    strings['body'] = owner_form % msg
    print 'Content-Type: text/html\n'
    print HTML_TEMPLATE % strings

# Handles if user is logged in, and what request method calls for the script.
def main():
    if not isLoggedIn():
        REDIRECT('login.html')
    else:
        db = Database()
        if not db.isOwnerFromCookie():
            REDIRECT('gallery.cgi')

    if os.environ['REQUEST_METHOD'] == 'GET':
        print 'Content-Type: text/html\n'
        print HTML_TEMPLATE % strings

    else:
        ownerActions()

main()
