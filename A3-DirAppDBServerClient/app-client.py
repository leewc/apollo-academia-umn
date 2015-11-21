#! /usr/bin/python3

from socket import *
import sys  # for CLI
import os

class App_client:
    def __init__(self, ds_port, db_port):
        # self.server = 'localhost' 
        self.dbserver = 'localhost' # change this if not running dbServer on atlas.cselabs.umn.edu

        self.ds_port = ds_port
        self.db_port = db_port
        self.appserver_list = list()
        self.client_socket = socket(AF_INET,SOCK_STREAM)


    def start(self):
        self.getAppServerList()
        if len(self.appserver_list) < 1:
            return False
        appServer = self.appserver_list[0] # pick the first one for now.
        self.client_socket.connect(appServer)
        print("Connected to app-server: ", appServer)
        return True

        
    def getAppServerList(self):
        print("Connecting to dir-server for list of app-servers...")
        db_connection = socket(AF_INET, SOCK_STREAM)
        db_connection.connect( (self.dbserver, self.db_port) )
        db_connection.send(stob("list-servers\r\n"))

        response = self.receive_till_delim(db_connection)
        if 'success' in response:
            self.appserver_list = [(x, int(y)) for x,y in (z.split(' ') 
                                    for z in response.split('\r')[1:]) ] 
            #remove success msg, split each entry into tuple ip, port
        else:
            print("No app-servers found.")
        db_connection.close()

    def sendfiles(self, filenames):
        """Wrapper functuin that sends a list of files using transfer_file"""
        for filename in filenames:
            print("Sending file: ", filename)
            if app_client.transfer_file(filename):
                print("File transfer complete.")

    
    def transfer_file(self, filename):
        self.client_socket.send( stob("file " + filename + " " + str(os.path.getsize(filename)) + "\r\n") )
        resp = self.receive_till_delim(self.client_socket)
        if 'begin' in resp:
            with open(filename, 'rb') as file:

                while True:
                    chunk = file.read(1024)    
                    if not chunk:
                        break
                    self.client_socket.send(chunk)

            self.client_socket.send( stob("complete\r\n" ) )
            resp = self.receive_till_delim(self.client_socket)
            if 'success' in resp:
                return True
        return False

    def receive_till_delim(self, connection_socket):
        message = ""
        while '\r\n' not in message:
           chunk = connection_socket.recv(1024)
           message += chunk.decode('ascii')
           if len(chunk) == 0:
               break;
        return message.rstrip('\r\n') # remove the ending delimiter    

    def shutdown(self):
        self.client_socket.close()

def stob(string):
    """strToBytes
    - Converts an ASCII string into bytes to be sent over the socket
    - Note the provided DB-server in C doesn't need it as ASCII, and Python defaults to UTF-8,
      but we should nonetheless set a standard."""
    return string.encode(encoding='ASCII')

def main(argv):
    if len(argv) < 3:
        print("Usage: %s <ds_port> <db_port>" % argv[0])
        return False

    try:
        app_client = App_client(int(argv[1]), int(argv[2]))
        started = app_client.start()

        if not started:
            print("Failed to start client. Shutting down.")
            app_client.shutdown()
            return

        filenames = ['1000k.dat']
        app_client.sendfiles(filenames)
        
        app_client.shutdown()

        return True

    except KeyboardInterrupt:
        print("CTRL-C pressed, shutting down.")
        app_client.shutdown()
        sys.exit()

    # except Exception as e:
    #     print("Error. <ds_port> is not an integer or something went wrong..")
    #     print("Stack Trace: ")
    #     print (e)
    #     app_serv.shutdown()
    #     return False


if __name__ == "__main__":
    main(sys.argv)
