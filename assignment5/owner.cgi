#!/usr/bin/python
import cgi
import os

from shared import *
from database import *

import cgitb
cgitb.enable()

# make sure to put a string in for msg.
owner_form = """
<form name="ownerForm" action="owner.cgi" method="POST" enctype="multipart/form-data">
 %s
 <h2> Add a User </h2>
 Username: <input type='text' name='newUsername' />
 <br/>
 Password: <input type='password' name='password' />
 <br/>

 <h2> Delete a User </h2>
 Username to delete: <input type='text' name='deleteUsername' />
 <br/>

 <h2> Change User Password </h2>
 Username: <input type='text' name='changepwdUsername' />
 New Password: <input type='password' name='newPassword'/> 
 <br/>

  button to go to gallery! and upload etc
<input type="submit" value="Log In" />
</form>
"""


def main():
    if not isLoggedIn():
        REDIRECT('login.html')
    else:
        db = Database()
        if not db.isOwnerFromCookie():
            REDIRECT('gallery.cgi')



main()
