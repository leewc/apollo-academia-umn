package server;

import shared.*;

import java.io.*;
import java.net.*;

class TCPServer 
{
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
		System.out.println("server: RX <msg_type> <cur_seq> <max_seq> <payload_len>");
		while(true) 
         {
            Socket connectionSocket = serverSocket.accept();
            
            if(MsgT.DEBUG)
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
		

		switch(recv.msgType)
		{
			case MsgT.MSG_TYPE_GET:
				FileInputStream fstream = getFile(new String(recv.getPayload()));
				if(fstream != null)
				{
					System.out.println("HOLY SHIT THIS WORKS");
				}
				break;
			case MsgT.MSG_TYPE_GET_ACK:
				break;
			case MsgT.MSG_TYPE_FINISH:
				break;
			default:
				if(MsgT.DEBUG) System.err.println("DO NOT UNDERSTAND MSG_TYPE");
				throw new UnsupportedOperationException();
		}


		if(MsgT.DEBUG) System.out.println("\n Content " + new String (recv.getPayload()));
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

    public FileInputStream getFile(String fileName)
    {
    	FileInputStream fstream = null;
    	try 
    	{
    		File file = new File(curDir, fileName);
    		fstream = new FileInputStream(file);
    	}
    	catch (FileNotFoundException e)
    	{
    		if(MsgT.DEBUG) System.out.println(fileName + " requested by client but not found.");
    	}
    	finally
    	{
    		return fstream;
    	}
    }
}
