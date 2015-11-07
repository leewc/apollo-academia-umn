#!/usr/bin/python
import os
from shared import *
from login import isLoggedIn, Database
class ImageTile():
	"""Class that holds the thumbnails and photo paths, used for easy generation of page.
	fileName should be without the extension, so we can refer to the thumbnail and text
	"""
	def __init__(self, fileName):
		self.fileName = fileName[:-4] # safe because we control what format goes in that folder
		self.filePath = os.path.join(UPLOAD_DIR, self.fileName) #also of no extension
		self.imgFilePath = self.filePath + ".jpg"
		self.title = getTitle(self.filePath + ".txt") # method from shared
		self.thumbnail = self.filePath + "_tn.jpg"

	def tile(self):
		return """<img id="%(filename)s" src="%(thumbnail)s" onclick="fbox(this)" alt="%(filePath)s" />
				<h1 id="title-%(filename)s"> %(title)s </h1>
				<a href="delete.cgi?id=%(filename)s"> Delete </a>
				<a href="edit.cgi?id=%(filename)s"> Edit </a> 
		""" % {'thumbnail': self.thumbnail, 'filePath': self.filePath, 
				'title': self.title, 'filename': self.fileName}

def generateTiles():
	listOfFiles = os.listdir(UPLOAD_DIR)
	pictures = []
	htmlString = "<tr>" # start table row
	for a in range(len(listOfFiles)):
		if '.txt' in listOfFiles[a]: # string checking has issues, avoid _tn, just use txt. 
			pictures.append(listOfFiles[a])
		# if '.txt' == fileName[-4:] or 'tn' == fileName[-6:-4]:
		# if "_tn" in fileName or ".txt" in fileName: # it's werid this doesn't work...
	for i in range(len(pictures)):
		if(i%4 == 0 and i != 0):
			htmlString += "</tr> <tr>" #next row
		htmlString += "<td>%(tile)s</td>" % {'tile': ImageTile(pictures[i]).tile()}
	htmlString += "</tr>"
	return htmlString

body = """<div id="buttons"><a href="gallery.cgi"><button type=button>Refresh</button></a> 
		  <a href="upload.cgi"><button type=button>Upload New Picture</button></a></div>
                   <br/>
		  <table>
		  	%(allTiles)s
		  </table>
	   """ % { 'allTiles': generateTiles() }

fboxScript="""
<script>
function fbox(img){
	var title = document.getElementById('title-' + img.id);
	var screen = document.createElement('div');
	screen.id = "screen";
	screen.innerHTML = title.outerHTML + "<img src='pictures/" + img.id +".jpg' /> ";
	screen.onclick = function(){
					var screen = document.getElementById("screen");
					screen.parentNode.removeChild(screen);
	}
	document.body.insertBefore(screen, document.body.firstChild);
}
</script>"""

strings = {
	'windowTitle': "Picture Gallery",
	'title': "Picture Gallery",
	'body': body + fboxScript
}

print 'content-type: text/html\n'
print HTML_TEMPLATE % strings
