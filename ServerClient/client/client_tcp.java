package client;

import shared.*;
import java.net.*;

public class client_tcp {
	//Driver class that starts a TCPClient instance based on cmd commands
	public static int port;

	public static void main(String[] args) {
		if(args.length < 3){
			System.err.println("Usage: java client.client_tcp <server-ip> <port> <filename>");
			return;	
		}

		port = Integer.parseInt(args[1]);
		TCPClient tcpClient;
		try
		{
			tcpClient = new TCPClient(args[0], port); //localhost = 127.0.0.1
			System.out.println("client: RX <msg_type> <cur_seq> <max_seq> <payload_len>");

			Boolean status = tcpClient.getFileFromServer(args[2].toCharArray());
            
			if(status)
				System.out.println("File Download Complete.");

			tcpClient.closeSocket();
		}
		catch (ConnectException e)
		{
			System.err.println("Connection Refused, no server found at that port.");
		}
		catch (SocketException e)
		{
			System.err.println("Connection Reset by Server.");
			if(MsgT.DEBUG) e.printStackTrace();
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
	}

}
