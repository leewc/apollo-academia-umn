package server;

import shared.*;

import java.io.*;
import java.net.*;

class TCPServer 
{
	public static final int BUFFER_SIZE = 256;
	public int port;
	public ServerSocket serverSocket;
	public final File curDir;

	public TCPServer(int port, File curDir) throws Exception
	{
		this.serverSocket = new ServerSocket(port);
		this.curDir = curDir;
	}

	public void start() throws Exception
	{
		while(true) 
         {
            Socket connectionSocket = serverSocket.accept();
            System.out.println("Client Connected at port number:" + connectionSocket.getLocalPort());
            
            ObjectInputStream inFromClient = new ObjectInputStream(connectionSocket.getInputStream());
            ObjectOutputStream outToClient = new ObjectOutputStream(connectionSocket.getOutputStream());
            
            processRequest(inFromClient, outToClient);
            
         }
	}

	public void processRequest(ObjectInputStream inFromClient, ObjectOutputStream outToClient) throws Exception
	{
		Message recv = (Message) inFromClient.readObject(); //deserialize
		System.out.println("server: RX " + recv.getStatus());
		System.out.println("Content " + new String (recv.getPayload()));
	}

	//Credit: http://stackoverflow.com/questions/1844688/read-all-files-in-a-folder
	public void listFilesForFolder(final File folder) {
    for (final File fileEntry : folder.listFiles()) {
        if (fileEntry.isDirectory()) {
            listFilesForFolder(fileEntry);
        } else {
            System.out.println("\t server/" + fileEntry.getName());
        }
    }
}
}