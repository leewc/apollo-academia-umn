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
		// while(true) //commenting this out since we don't have to keep it alive after servicing a request 
         // {
            Socket connectionSocket = serverSocket.accept();
            
            if(MsgT.DEBUG) System.out.println("Client Connected at port number:" + connectionSocket.getLocalPort());

            System.out.println("server: RX <msg_type> <cur_seq> <max_seq> <payload_len>");
            
            ObjectInputStream inFromClient = new ObjectInputStream(connectionSocket.getInputStream());
            ObjectOutputStream outToClient = new ObjectOutputStream(connectionSocket.getOutputStream());
            
            processRequest(inFromClient, outToClient);
         // }
	}

	/* Recursive function that will keep waiting for requests unti it receives finish signal! */
	public void processRequest(ObjectInputStream inFromClient, ObjectOutputStream outToClient) throws Exception
	{
		Message recv = (Message) inFromClient.readObject(); //deserialize
		Message send;

		while(recv.msgType != MsgT.MSG_TYPE_FINISH)
		{
			System.out.println("server: RX " + recv.getStatus());
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
					// if(MsgT.DEBUG)	System.out.println("server: TX " + send.getStatus());
					break;

				case MsgT.MSG_TYPE_GET_ACK:
					send = getChunk();
					outToClient.writeObject(send);
					// if(MsgT.DEBUG) 	System.out.println("server: TX " + send.getStatus());
					break;

				default:
					if(MsgT.DEBUG) 	System.err.println("DO NOT UNDERSTAND MSG_TYPE");
					throw new UnsupportedOperationException();
			}
			recv = (Message) inFromClient.readObject();
			// if(MsgT.DEBUG) System.out.println("\n Content " + new String (recv.getPayload());
		}
		//Exit while loop, received finished message.
		System.out.println("server: RX " + recv.getStatus()); //print final status
		if(buffered_rdr != null)
			buffered_rdr.close();
		cur_seq = 0;
		max_seq = 0;

		if(MsgT.DEBUG) 	System.out.println("Client Request complete.");
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
		//Got to check for buffer size first, else we over read() and eat a byte which gets lost.
		while( index != MsgT.BUFFER_SIZE && (r = buffered_rdr.read()) != -1)
		{
			payload[index] = (char) r;
			index++;
		}
		cur_seq ++;

		if(cur_seq > max_seq) //this will happen when EOF
		{
			if(MsgT.DEBUG)
				System.out.println("Complete transfer.");
			return new Message(MsgT.MSG_TYPE_FINISH, new char[0], 0); 
		}

		// improvement: look at mark(int readLimit) for buffered reader to resume from error
		return new Message(MsgT.MSG_TYPE_GET_RESP, cur_seq, max_seq, index, payload);
	}

    public FileInputStream getFile(String fileName)
    {
    	FileInputStream fstream = null;
    	try 
    	{
    		File file = new File(curDir, fileName);
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
