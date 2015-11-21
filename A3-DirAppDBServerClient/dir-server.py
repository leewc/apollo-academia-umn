#! /usr/bin/python3

from socket import *
import sys  # for CLI

class Dir_server(): # http://stackoverflow.com/q/15374857/ (it don't matter anymore)
    """A single threaded server that keeps track of the app_servers"""
    def __init__(self,ds_port):
        self.hostname = 'localhost'
        self.app_server_list = list()
        self.ds_port = ds_port
        self.server_socket = socket(AF_INET, SOCK_STREAM)

    def start(self):
        self.server_socket.bind((self.hostname, self.ds_port))
        self.server_socket.listen(1)
        print("dir-server: Listening for connections ... (type Ctrl-C to exit)")

        while True:
            connection_socket, addr = self.server_socket.accept() #returns tuple (conn, address)
            print("Client Connected.")

            while True:
                message = self.receive_till_delim(connection_socket)
                if len(message) == 0:
                    break #connection closed, next client. 
                print("RX: ", message)
                self.processMessage(connection_socket, message)

    def processMessage(self, connection_socket, message):
        fail = False
        split = message.split(' ')
        try:
            if len(split) == 3 and split[0] == "register":
                entry = split[1] + " " + split[2] # <ip> <port>
                self.app_server_list.append(entry)
                connection_socket.send(stob("success\r\n"))

            elif len(split) == 1 and split[0] == "list-servers":
                if(len(self.app_server_list) == 0):
                    fail = True
                else:
                    connection_socket.send(stob("success\r" + self.get_server_strlist() + '\n' ))

            else:
                print("Do not understand message.") # drop it
                fail = True
        except:
            fail = True
            print("Error.")

        if fail:
            connection_socket.send(stob("failure\r\n"))
            return False
        return True

    def receive_till_delim(self, connection_socket):
        message = ""
        while '\r\n' not in message:
           chunk = connection_socket.recv(1024)
           message += chunk.decode('ascii')
           if len(chunk) == 0:
               break;
        return message.rstrip('\r\n') # remove the ending delimiter

    def get_server_strlist(self):
        """returns a stringified version of the entries in the app_server"""
        return "".join([entry + '\r' for entry in self.app_server_list])

    def shutdown(self):
        self.server_socket.close()

def stob(string):
    """strToBytes
    - Converts an ASCII string into bytes to be sent over the socket
    - Note the provided DB-server in C doesn't need it as ASCII, and Python defaults to UTF-8,
      but we should nonetheless set a standard."""
    return string.encode(encoding='ASCII')

def main(argv):
    if len(argv) < 2:
        print("Usage: %s <ds_port>" % argv[0])
        return False

    try:
        dir_serv = Dir_server(int(argv[1]))
        dir_serv.start()
        
        return True

    except KeyboardInterrupt:
        print("CTRL-C pressed, shutting down.")
        dir_serv.shutdown()
        sys.exit()

    # except Exception as e:
    #     print("Error. <ds_port> is not an integer or something went wrong..")
    #     print("Stack Trace: ")
    #     print (e)
    #     return False

if __name__ == "__main__":
    main(sys.argv)