package server;

import shared.*;

import java.io.*;
import java.net.*;
import java.lang.Math;

/* A simple TCP Server that will wait for a client to connect at a socket, and then serve files
 * in the local directory.
*/
class TCPServer 
{
	public int port;
	public ServerSocket serverSocket;
	public final File curDir;

	private Reader buffered_rdr;
	private int cur_seq;
	private int max_seq;

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
            
            if(MsgT.DEBUG) System.out.println("Client Connected at port number:" + connectionSocket.getLocalPort());

            System.out.println("server: RX <msg_type> <cur_seq> <max_seq> <payload_len>");
            
            ObjectInputStream inFromClient = new ObjectInputStream(connectionSocket.getInputStream());
            ObjectOutputStream outToClient = new ObjectOutputStream(connectionSocket.getOutputStream());
            
            processRequest(inFromClient, outToClient);
         }
	}

	/* Recursive call that will keep waiting for requests! */
	public void processRequest(ObjectInputStream inFromClient, ObjectOutputStream outToClient) throws Exception
	{
		Message recv = (Message) inFromClient.readObject(); //deserialize
		System.out.println("server: RX " + recv.getStatus());
		Message send;

		switch(recv.msgType)
		{
			case MsgT.MSG_TYPE_GET: //only one first get call each time.
				FileInputStream fs = getFile(new String(recv.getPayload()));
				if(fs != null) //getFile will have generated a stream by then.
				{
					//max seq is set by getFile
					cur_seq = 0;
					buffered_rdr = new BufferedReader(new InputStreamReader(fs, "US-ASCII"));
					send = getChunk();
				}
				else
				{
					send = new Message(MsgT.MSG_TYPE_GET_ERR, new char[0], 0);
				}

				outToClient.writeObject(send);

				if(MsgT.DEBUG)
						System.out.println("server: TX " + send.getStatus());
				processRequest(inFromClient, outToClient);
				
				break;
			case MsgT.MSG_TYPE_GET_ACK:
				send = getChunk();
				
				outToClient.writeObject(getChunk());

				if(MsgT.DEBUG)
						System.out.println("server: TX " + send.getStatus());
				processRequest(inFromClient, outToClient);
				break;

			case MsgT.MSG_TYPE_FINISH:
				buffered_rdr.close();
				System.out.println("WE DONE");
				break;
			default:
				if(MsgT.DEBUG) System.err.println("DO NOT UNDERSTAND MSG_TYPE");
				throw new UnsupportedOperationException();
		}
		// if(MsgT.DEBUG) System.out.println("\n Content " + new String (recv.getPayload()));
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

	public Message getChunk() throws FileNotFoundException, IOException
	{
		char[] payload = new char[MsgT.BUFFER_SIZE];
		int r;
		int index = 0;
		while(  (r = buffered_rdr.read()) != -1 && index != MsgT.BUFFER_SIZE - 1)
		{
			payload[index] = (char) r;
			index++;
		}
		cur_seq ++;

		System.out.println("CUR " + cur_seq + " MAX " + max_seq);
		
		if(cur_seq > max_seq) //this will happen when EOF
		{
			System.out.println("Complete transfer.");
			return new Message(MsgT.MSG_TYPE_FINISH, new char[0], 0); 
		}

		// improvement: look at mark(int readLimit) for buffered reader to resume from error
		return new Message(MsgT.MSG_TYPE_GET_RESP, cur_seq, max_seq, index+1, payload);
	}

    public FileInputStream getFile(String fileName)
    {
    	FileInputStream fstream = null;
    	try 
    	{
    		File file = new File(curDir, fileName);
    		file.setReadOnly();
    		fstream = new FileInputStream(file);
    		max_seq = (int) Math.ceil(file.length() / (double) MsgT.BUFFER_SIZE);	//THIS IS UNSAFE, CHECK WITH REQS

    		if(MsgT.DEBUG)
    			System.out.println("MAX_SEQ " + max_seq + "FS " + file.length());
    	}
    	catch (FileNotFoundException e)
    	{
    		if(MsgT.DEBUG) System.out.println(fileName + " requested by client but not found. Sending Error Response.");
    	}
    	finally
    	{
    		return fstream;
    	}
    }
}
