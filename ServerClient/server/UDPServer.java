package server;

import shared.*;

import java.io.*;
import java.net.*;
import java.lang.Math;

/* A simple UDP Server that will wait for a client to connect at a socket, and then serve files
 * in the local directory.
*/
class UDPServer 
{
	public int port;
	public DatagramSocket serverSocket;
	public final File curDir;

	public InetAddress clientInet;

	private Reader buffered_rdr;
	private int cur_seq;
	private int max_seq;

	public UDPServer(int port, File curDir) throws Exception
	{
		this.serverSocket = new DatagramSocket(port);
		this.curDir = curDir;
	}

	public void start() throws Exception
	{
		// while(true) //commenting this out since we don't have to keep it alive after servicing a request 
         // {
			System.out.println("server: RX <msg_type> <cur_seq> <max_seq> <payload_len>");

            this.processRequest();

            System.out.println("Shutting Server Down.");
         // }
	}

	/* Function that will keep waiting for requests unti it receives finish signal! */
	public void processRequest() throws Exception
	{
		Message recv = getAndDeserializeFromClient(); //deserialize
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

					writeToClient(send);
					// if(MsgT.DEBUG)	System.out.println("server: TX " + send.getStatus());
					break;

				case MsgT.MSG_TYPE_GET_ACK:
					send = getChunk();
					writeToClient(send);
					// if(MsgT.DEBUG) 	System.out.println("server: TX " + send.getStatus());
					break;

				default:
					if(MsgT.DEBUG) 	System.err.println("DO NOT UNDERSTAND MSG_TYPE");
					throw new UnsupportedOperationException();
			}
			recv = getAndDeserializeFromClient();
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

	//Also updates the client Inet
	public Message getAndDeserializeFromClient() throws IOException, ClassNotFoundException
	{
		//create a larger than needed ByteArray for deserialization to avoid truncation
		byte[] buffer = new byte[4096];
		DatagramPacket recvPacket = new DatagramPacket(buffer, buffer.length);
		this.serverSocket.receive(recvPacket);

		this.clientInet = recvPacket.getAddress();
		if(MsgT.DEBUG) System.out.println("BEFORE PORT Assignment: " + port);
		//This prevents IOException when sending (caused by sending to a port it has no permissions to send to)
		//Although after testing it sends to literally the same port number. 
		this.port = recvPacket.getPort(); 
		if(MsgT.DEBUG) System.out.println("AFTER PORT Assignment from packet: " + port);

		ByteArrayInputStream baiStream = new ByteArrayInputStream(buffer);
		ObjectInputStream is = new ObjectInputStream( new BufferedInputStream(baiStream));

		Message recv = (Message) is.readObject();
		is.close();

		return recv;
	}

	public void writeToClient(Object obj) throws IOException  
	{
		//Serialize the Message object into bytes using a stream
		ByteArrayOutputStream baoStream = new ByteArrayOutputStream();
		//Defer the stream with buffer, ObjectOutputStream serializes the Object
		ObjectOutputStream os = new ObjectOutputStream(new BufferedOutputStream(baoStream));

		os.writeObject(obj);
		os.flush(); //force flush to retrieve all bytes

		//Get byteArrayFromStream to send off.
		byte[] serialized = baoStream.toByteArray();

		//Create packet for transmission
		DatagramPacket packet = new DatagramPacket(serialized, serialized.length, clientInet, port);

		serverSocket.send(packet); 

		os.close();
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
