#! /usr/bin/python3

from socket import *
import sys  # for CLI

class App_server():
    """A single threaded server that keeps track of the app_servers"""
    def __init__(self, ds_port):
        self.dir_hostname = 'apollo.cselabs.umn.edu' # where the dir-server is located at, change to apollo
        self.ds_port = ds_port
        self.server_socket = socket(AF_INET, SOCK_STREAM)

    def start(self):
        self.server_socket.bind(('', 0)) # empty string as hostname for local host
        print("app-server: Socket Bound to following IP and Port:")
        print(gethostbyname(gethostname()), ",", self.server_socket.getsockname()[1])

        if self.register_dir():
            print("Registration with dir-server successful.")
        else:
            print("Failed to register.")
            return

        # listen once we have registered
        self.server_socket.listen(1)
        print("app-server: Listening for connections ... (type Ctrl-C to exit)")

        while True:
            connection_socket, addr = self.server_socket.accept() #blocking, returns tuple (conn, address)
            print("Client Connected.")

            while True:
                message = self.receive_till_delim(connection_socket)
                if len(message) == 0:
                    break #connection closed, next client. 
                print("app-server RX: ", message)
                self.processMessage(connection_socket, message)

    def register_dir(self):
        register_socket = socket(AF_INET,SOCK_STREAM)
        register_socket.connect( (self.dir_hostname, self.ds_port) )
        register = "register " + str(gethostbyname(gethostname())) + " " + str(self.server_socket.getsockname()[1]) +"\r\n"
        register_socket.send( stob(register) )
        reply = self.receive_till_delim(register_socket)

        print("app-server: (Reponse from dir-server) ", reply)

        if 'success' in reply:
            return True
        return False

    def processMessage(self, connection_socket, message):
        fail = False
        split = message.split(' ')
        try:
            if len(split) == 3 and split[0] == "file": # file myfile.ext size
                filename = split[1]
                fileSize = int(split[2])

                connection_socket.send(stob("begin\r\n"))
                # begin subroutine that waits for file.
                self.receive_file(connection_socket, filename, fileSize)

            elif len(split) == 1 and split[0] == "complete":
                connection_socket.send(stob("success\r\n"))
                print("Ready for next file or client.")

            else:
                print("Do not understand message. Something went wrong.") # drop it
                fail = True
        except Exception as e:
            print( e)
            fail = True
            print("Error.")

        if fail:
            connection_socket.send(stob("failure\r\n"))
            return False
        return True

    def receive_file(self, connection_socket, filename, fileSize):
        received = 0
        with open("downloaded_"+filename, 'wb') as file:
            while received < fileSize:
                data = connection_socket.recv(1024)
                if not data:
                    break
                file.write(data)
                received += len(data)
                print("Received ... ", received, " of ", fileSize, end ="\r")
        print("\nTransfer complete...")
        return True

    def receive_till_delim(self, connection_socket):
        message = ""
        while '\r\n' not in message:
           chunk = connection_socket.recv(1024)
           message += chunk.decode('ascii')
           if len(chunk) == 0:
               break;
        return message.rstrip('\r\n') # remove the ending delimiter

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
        app_serv = App_server(int(argv[1]))
        app_serv.start()
        app_serv.shutdown()

        return True

    except KeyboardInterrupt:
        print("CTRL-C pressed, shutting down.")
        app_serv.shutdown()
        sys.exit()

    except Exception as e:
         print("Error. Something went wrong..")
         print("Stack Trace: ")
         print (e)
         app_serv.shutdown()
         return False

if __name__ == "__main__":
    main(sys.argv)
