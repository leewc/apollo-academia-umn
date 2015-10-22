package client;

import shared.*;

import java.io.*;
import java.net.*;


public class TCPClient {
	String serverIP; //Leave it as string for now, since there is a constructor for it
	int port;
	Socket clientSocket;
	ObjectOutputStream outToServer;
	ObjectInputStream inFromServer;

	BufferedWriter writer;
	String fileName;
	
	public TCPClient(String serverIP, int port) throws IOException
	{
		this.serverIP = serverIP;
		this.port = port;
		createSocket();

		this.outToServer = new ObjectOutputStream(clientSocket.getOutputStream());
		this.inFromServer = new ObjectInputStream(clientSocket.getInputStream());
		this.writer = null;
	}
	
	public void writeToServer(Object obj) throws IOException  
	{
		this.outToServer.writeObject(obj);
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
		Message recv = (Message) inFromServer.readObject(); //deserialize
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
			recv = (Message) inFromServer.readObject();
		}
		//Exit while loop
		System.out.println("client: RX " + recv.getStatus());
		
		if(MsgT.DEBUG)
			System.out.println("Downloaded file: " + System.getProperty("user.dir") + "/"+ fileName);

		send = new Message(MsgT.MSG_TYPE_FINISH, new char[0], 0);
		writeToServer(send);
		writer.close();
		return true;
		// if(send != null && MsgT.DEBUG)
			// System.out.println("client: TX " + send.getStatus());
	}

	public void createSocket() throws IOException, ConnectException
	{
		System.out.println("Creating socket on host: " + serverIP);
		clientSocket = new Socket(serverIP, port);
		System.out.println("Client Connection Established");
		if(clientSocket.getPort() == 0)
			System.err.println("Socket not connected yet");
	}
	
	public void closeSocket() throws IOException
	{
		clientSocket.close();
	}
	
	

}
