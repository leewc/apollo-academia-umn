package client;

import shared.*;
import java.net.*;

public class client_udp {
	//Driver class that starts a TCPClient instance based on cmd commands
	public static int port;

	public static void main(String[] args) {
		if(args.length < 3){
			System.err.println("Usage: java client.client_udp <server-ip> <port> <filename>");
			return;	
		}

		port = Integer.parseInt(args[1]);
		UDPClient udpClient;
		try
		{
			udpClient = new UDPClient(args[0], port); //localhost = 127.0.0.1
			System.out.println("client: RX <msg_type> <cur_seq> <max_seq> <payload_len>");

			Boolean status = udpClient.getFileFromServer(args[2].toCharArray());
            
			if(status)
				System.out.println("File Download Complete.");
			else
				System.err.println("File not found on Server.");

			udpClient.closeSocket();
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
