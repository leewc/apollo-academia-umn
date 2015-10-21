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
	
	public TCPClient(String serverIP, int port) throws IOException
	{
		this.serverIP = serverIP;
		this.port = port;
		createSocket();

		this.outToServer = new ObjectOutputStream(clientSocket.getOutputStream());
		this.inFromServer = new ObjectInputStream(clientSocket.getInputStream());
	}
	
	public void writeToServer(Object obj) throws IOException  
	{
		this.outToServer.writeObject(obj);
	}

	//This class is the main class that will do all file and packet operations
	public Boolean getFileFromServer(char[] fileName) throws IOException, ClassNotFoundException
	{
		char[] payload = new char[MsgT.BUFFER_SIZE];
		
		for(int i = 0; i < fileName.length; i++)
		{
			payload[i] = fileName[i];
		}

		Message getMsg = new Message(MsgT.MSG_TYPE_GET, payload, fileName.length);
		writeToServer(getMsg);
		
		return getResponseFromServer();
	}
	
	public Boolean getResponseFromServer() throws IOException, ClassNotFoundException
	{
		Message recv = (Message) inFromServer.readObject(); //deserialize
		System.out.println("client: RX " + recv.getStatus());
		return true;
		// int count;
		// char[] buffer = new char[8192]; 
		// while ((count = inFromServer.read(buffer)) > 0)
		// {
		//   inFromServer.write(buffer, 0, count);
		// }
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
