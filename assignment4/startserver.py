#!/usr/bin/env python

"""
Driver that starts a local server for local development.
Credit: https://pointlessprogramming.wordpress.com/2011/02/13/python-cgi-tutorial-1/

CGI scripts run by the CGIHTTPRequestHandler class cannot execute redirects (HTTP code 302),
because code 200 (script output follows) is sent prior to execution of the CGI script.
This pre-empts the status code.
"""
import BaseHTTPServer
import CGIHTTPServer
import cgitb
cgitb.enable()  # This line enables CGI error reporting

server = BaseHTTPServer.HTTPServer
handler = CGIHTTPServer.CGIHTTPRequestHandler
server_address = ("", 8000)
handler.cgi_directories = ["/"]

print "Server is listening on port: " + str(server_address[1]) + " ....."

httpd = server(server_address, handler)
httpd.serve_forever()
