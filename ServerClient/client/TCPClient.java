package client;

import shared.*;

import java.io.*;
import java.net.*;


public class TCPClient {
	String serverIP; //Leave it as string for now, since there is a constructor for it
	int port;
	Socket clientSocket;
	ObjectOutputStream outToServer;
	BufferedReader inFromServer;
	
	public TCPClient(String serverIP, int port) throws IOException
	{
		this.serverIP = serverIP;
		this.port = port;
		createSocket();

		this.outToServer = new ObjectOutputStream(clientSocket.getOutputStream());
		this.inFromServer = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
	}
	
	public void writeToServer(Object obj) throws IOException  
	{
		this.outToServer.writeObject(obj);
	}

	public Boolean getFileFromServer(String fileName) throws IOException
	{
		char[] payload = new char[256];

		Message getMsg = new Message(MsgT.MSG_TYPE_GET, payload, fileName.length());
		writeToServer(getMsg);
		return true;
	}
	
	public void readLineFromServer() throws IOException
	{
		System.out.println("Reading a line from the server.");
		String x;

		while((x = inFromServer.readLine()) != null)
		{
			System.out.println("X IS: " + x.toString());
		}
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
			System.out.print("Socket not connected yet");
	}
	
	public void closeSocket() throws IOException
	{
		clientSocket.close();
	}
	
	

}
