#! /usr/bin/python3

from socket import *
import sys  # for CLI
import os

import time # for test runs

class App_client:
    def __init__(self, ds_port, db_port):
        # self.server = 'localhost' 
        self.dbserver = 'localhost' # change this if not running dbServer on atlas.cselabs.umn.edu
        self.dir_server = 'localhost'
        self.testRuns = 5

        self.ds_port = ds_port
        self.db_port = db_port
        self.appserver_list = list()
        self.selectedAppServer = None
        self.client_socket = socket(AF_INET,SOCK_STREAM)
        self.db_socket = socket(AF_INET, SOCK_STREAM)

    def start(self):
        self.getAppServerList()
        if len(self.appserver_list) < 1:
            return False
        self.selectedAppServer = self.appserver_list[0] # pick the first one for now.
        
        self.client_socket.connect(self.selectedAppServer)
        print("Connected to app-server: ", self.selectedAppServer)
        
        self.db_socket.connect( (self.dbserver, self.db_port) )
        print("Connected to db-server: ", (self.dbserver, self.db_port))

        return True
        
    def getAppServerList(self):
        print("Connecting to dir-server for list of app-servers...")
        dir_connection = socket(AF_INET, SOCK_STREAM)
        dir_connection.connect( (self.dir_server, self.ds_port) )
        dir_connection.send(stob("list-servers\r\n"))

        response = self.receive_till_delim(dir_connection)
        if 'success' in response:
            self.appserver_list = [(x, int(y)) for x,y in (z.split(' ') 
                                    for z in response.split('\r')[1:]) ] 
            #remove success msg, split each entry into tuple ip, port
            for line in response.split('\r'):
                print(line)
        else:
            print("No app-servers found.")
        dir_connection.close()

    def sendfiles_test(self, filenames):
        """Wrapper function that sends a list of files using transfer_file"""
        for filename in filenames:
            print("Performing file transfer tests on file: ", filename)
            t_total = 0
            for i in range(self.testRuns):
                t_start = time.time()
                if self.transfer_file(filename):
                    t_elapsed = time.time() - t_start
                    print("Completed trial: ", i+1, "Time: ", t_elapsed)
                    t_total += t_elapsed
            t_average = t_total / self.testRuns
            print("Average time: ", t_average)
            self.send_stats(os.path.getsize(filename), t_average)
    
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
            print("RX :", resp)
            if 'success' in resp:
                return True
        return False

    def send_stats(self, filesize, t_avgUpload):
        print("Sending stats to db-server..") # gethostbyname(gethostname())
        self.db_socket.send( stob("set-record " + self.client_socket.getsockname()[0] + " " 
                                + self.selectedAppServer[0] + " " + str(self.selectedAppServer[1]) 
                                + " " + str(filesize) + " " + str(t_avgUpload) + "\r\n" ))
        resp = self.receive_till_delim(self.db_socket)
        if "success" in resp:
            print(resp)
            print("Stats recorded successfully.")
        else:
            print("Failed to send stats.")

    def get_db_stats(self):
        """Download and display db stats"""
        print("Getting records from db-server.")
        self.db_socket.send( stob("get-records\r\n") )
        resp = self.receive_till_delim(self.db_socket)
        # must split by '\r' else print only shows one line
        if 'success' in resp:
            print("<client_ip>  <server_ip>  <port>  <data_len>  <time>")
            for row in resp.split('\r')[1:]:
                print (row)

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

        # generate files this way: base64 /dev/urandom | head -c 100k > 100k.dat
        # filenames = ['10k.dat', '100k.dat', '1000k.dat', '10000k.dat']
        filenames = ['10k.dat', '100k.dat']
        app_client.sendfiles_test(filenames)
        app_client.get_db_stats()
        
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
