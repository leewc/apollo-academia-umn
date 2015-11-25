#!/usr/bin/python
import cgi
import os

from shared import *
from database import * 

import cgitb
cgitb.enable()


# This is needed since the landing page is login.html and there's no way to edit the static page. 
login_form = """
<form name="loginForm" action="login.cgi" method="POST" enctype="multipart/form-data">
 %s
 Username: <input type='text' name='username' />
 <br/>
 Password: <input type='password' name='password' />
 <br/>
<input type="submit" value="Log In" />
</form>
"""

msg = """<div id="message">Error: Invalid Username and/or Password. </div>"""
empty_msg = """<div id="message">Error: Please enter a username and password. </div>"""

def main():
    form = cgi.FieldStorage()

    if os.environ['REQUEST_METHOD'] == 'GET':
        # check if logged in
        if not isLoggedIn():
            REDIRECT('login.html')
        else:
            REDIRECT('gallery.cgi')
    else:
        db = Database()
        # Check for password or provide error (This is POST)
        username = form['username'].value
        password = form['password'].value
        if len(username) == 0 or len(password) ==0: 
            print HTML_TEMPLATE % {'windowTitle': 'Login Form', 
                                   'title' : 'Login', 
                                   'body' : (login_form % empty_msg) }
        else:
            if db.login(username, password): 
                db.makeCookie(username)
                REDIRECT('gallery.cgi')
            else:
                print HTML_TEMPLATE % {'windowTitle': 'Login Form', 
                                       'title' : 'Login', 
                                       'body' : (login_form % msg) }

main() # simple invocation
