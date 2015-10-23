package client;

import shared.*;

import java.io.*;
import java.net.*;


public class UDPClient {
	String serverIP; //Leave it as string for now, since there is a constructor for it
	int port;
	DatagramSocket clientSocket;
	InetAddress serverInet;

	BufferedWriter writer;
	String fileName;
	
	public UDPClient(String serverIP, int port) throws IOException
	{
		this.serverIP = serverIP;
		this.serverInet = InetAddress.getByName(serverIP);
		this.port = port;
		this.createSocket();

		this.writer = null;
	}
	
	public void writeToServer(Object obj) throws IOException  
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
		DatagramPacket packet = new DatagramPacket(serialized, serialized.length, serverInet, port);

		clientSocket.send(packet); 

		os.close();
	}

	public Message getAndDeserializeFromServer() throws IOException, ClassNotFoundException
	{
		//create a larger than needed ByteArray for deserialization to avoid truncation
		byte[] buffer = new byte[4096];
		DatagramPacket recvPacket = new DatagramPacket(buffer, buffer.length);
		this.clientSocket.receive(recvPacket);

		ByteArrayInputStream baiStream = new ByteArrayInputStream(buffer);
		ObjectInputStream is = new ObjectInputStream( new BufferedInputStream(baiStream));

		Message recv = (Message) is.readObject();
		is.close();

		return recv;
	}

	public Boolean getFileFromServer(char[] fileName) throws IOException, ClassNotFoundException
	{
		this.fileName = new String(fileName);

		char[] payload = new char[MsgT.BUFFER_SIZE];

		for(int i = 0; i < fileName.length; i++)
		{
			payload[i] = fileName[i];
		}

		Message getMsg = new Message(MsgT.MSG_TYPE_GET, payload, fileName.length);
		writeToServer(getMsg);
		
		return receiveFromServer();
	}
	
	//This class is the main class that will do all file and packet operations
	public Boolean receiveFromServer() throws IOException, ClassNotFoundException
	{
		long start = System.nanoTime();
		Message recv = getAndDeserializeFromServer(); //deserialize
		Message send; 
		
		while(recv.msgType != MsgT.MSG_TYPE_FINISH)
		{
			System.out.println("client: RX " + recv.getStatus());
			switch(recv.msgType)
			{
				case MsgT.MSG_TYPE_GET_RESP:
					if(writer == null) //First message, make a file and write out
					{
						writer = new BufferedWriter(
							new OutputStreamWriter(new FileOutputStream(fileName, false), "US-ASCII")); //C unsigned chars are ASCII 0-255 
						// writer = new FileWriter("fileName.txt", false);
						//Not using FileWriter because of encoding, bug was in index, not this.
					}
					writer.write(recv.getPayload());

					send = new Message(MsgT.MSG_TYPE_GET_ACK, new char[0], 0);
					writeToServer(send);
					break;

				case MsgT.MSG_TYPE_GET_ERR:
					send = new Message(MsgT.MSG_TYPE_FINISH, new char[0], 0);
					writeToServer(send);
					return false;

				default:
					System.err.println("CANNOT UNDERSTAND SERVER MSG RESPONSE.");
					throw new UnsupportedOperationException();
			}
			recv = getAndDeserializeFromServer();
		}
		//Exit while loop
		System.out.println("client: RX " + recv.getStatus());
		
		if(MsgT.DEBUG)
			System.out.println("Downloaded file: " + System.getProperty("user.dir") + "/"+ fileName);

		double elapsed_time = ((double) (System.nanoTime() - start )) / 1000000000.0;
		System.out.println("Elapsed Time to Download File in seconds: " + elapsed_time);

		send = new Message(MsgT.MSG_TYPE_FINISH, new char[0], 0);
		writeToServer(send);
		writer.close();
		return true;
		// if(send != null && MsgT.DEBUG)
			// System.out.println("client: TX " + send.getStatus());
	}

	public void createSocket() throws IOException, ConnectException
	{
		System.out.println("Creating UDP Socket on host: " + serverIP);
		// clientSocket = new DatagramSocket(port, serverInet);
		clientSocket = new DatagramSocket(null); //Cannot bind to the same port serverSocket is at.
		if(clientSocket.getPort() == 0)
			System.err.println("Socket not connected yet");
	}
	
	public void closeSocket() throws IOException
	{
		clientSocket.close();
	}

}
