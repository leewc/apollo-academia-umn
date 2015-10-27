#!/usr/bin/python

import cgi
import os
import time  # time for file name
import Image # for thumbnails :)
from shared import * # import common templates and variables
 
form = cgi.FieldStorage()

#  onClick="(function(){document.form["uploadForm"].onSubmit="return true";})
# that does not work. TODO: DO we need server side redirect for cancel?

uploadForm ="""
<form name="uploadForm" action="upload.cgi" method="POST" enctype="multipart/form-data" onSubmit="return checkFile()">
Title: <input name="title" type="text"></br>
File: <input name="file" type="file"></br>
<input name="submit" type="submit">
<a href="gallery.cgi"> <button type="button">Cancel</button></a>
</form>
"""

clientSideCheckScript = """
<script>
	function checkFile(){
		var fileName = document.forms["uploadForm"]["file"].value;
		var ext = fileName.split('.').pop().toString().toLowerCase();
		if (ext == null || (ext != "jpg" && ext != "jpeg")){
			var x = document.createElement('p');
			x.id = "warn";
			if(document.getElementById("warn") == null){
				x.innerHTML = "Please select a valid JPG/JPEG image";
				document.body.insertBefore(x, document.forms["uploadForm"]);
			}
			return false;
		}
		return true;
	}
</script>
"""

strings = {
	'windowTitle': "Upload New Photo",
	'title': "Upload A New JPEG Picture",
	'body': uploadForm + clientSideCheckScript
}


def generate_thumbnail(imageFile, saveThumbPathName):
	img = Image.open(imageFile)
	img.thumbnail(THUMBNAIL_SIZE)
	img.save(saveThumbPathName, 'JPEG')

def save_title(filename, title):
	with open(filename, 'w') as file:
		file.write(title)

def save_uploaded_file (form_field, upload_dir):
    fileName = str(time.time())
    saveFilePathName = os.path.join(upload_dir, fileName + ".jpg")
    saveThumbPathName = os.path.join(upload_dir, fileName + "_tn.jpg")
    saveTitlePathName = os.path.join(upload_dir, fileName + ".txt")
    if not form.has_key(form_field): 
    	strings['body'] = "Error: Please Try Again, File Not Uploaded Correctly. \n" + strings['body']
        print HTML_TEMPLATE % strings
        return
    fileitem = form[form_field]
    if not fileitem.file or len(fileitem.filename) ==0: 
    	strings['body'] = "Error: Please Try Again, Empty or Invalid File.\n" + strings['body'] 
        print HTML_TEMPLATE % strings
        return
    try:

        with open(saveFilePathName, 'wb') as file:
    	    chunk = fileitem.file.read(100000)
            if not chunk:
        	    return
            file.write(chunk)

        generate_thumbnail(saveFilePathName,saveThumbPathName)
        save_title(saveTitlePathName, form['title'].value)
        strings["body"] = "File Uploaded Successfully"
        print HTML_TEMPLATE % strings
    except Exception as e:
        strings['body'] = "Error: Please Try Again, File Might not be a valid JPEG. \n" + strings['body']
        print HTML_TEMPLATE % strings
        print e # comment this to hide exception/errors
        if os.path.isfile(saveFilePathName):
            os.remove(saveFilePathName)
        if os.path.isfile(saveTitlePathName):
            os.remove(saveTitlePathName)
    	if os.path.isfile(saveThumbPathName):
            os.remove(saveThumbPathName)

print 'content-type: text/html\n'

## This is what makes the cgi self contained and post to itself.
# Credit: http://www-users.cs.umn.edu/~tripathi/python/LectureExamples/helloSingleFile.py

# Client side check has removed need for nested ifs, but keeping this to ensure server has total control.
if 'file' in form and 'title' in form:
	# if 'cancel' in form:
			# print REDIRECT_TEMPLATE % { 'URL' : 'google.com'}
	if len(form['file'].value) > 0:
		if len(form['title'].value) > 0 and len(form['title'].value) < 100: # validate title is not empty (won't be in form if empty)
			save_uploaded_file ("file", UPLOAD_DIR)
		else:
			strings['body'] = "Picture Title Cannot Be Empty or Too Long." + strings['body']
			print HTML_TEMPLATE % strings
	else:
		print HTML_TEMPLATE % strings
else:
	print HTML_TEMPLATE % strings

