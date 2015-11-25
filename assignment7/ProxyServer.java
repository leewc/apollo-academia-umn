import java.util.Properties;
import java.util.logging;

import java.io.FileInputStream;
import java.io.IOException;

import java.net.Socket;
import java.net.serverSocket;

public class ProxyServer extends Thread
{
    Properties config;
    Socket client;

    public ProxyServer(String configFilename, Socket client)
    {
	this.config = readConfigFile(configFilename);
	this.client = client;

	System.out.println("HERE's the config file");
	readConfigFile(configFilename).list(System.out);
    }
    
    public Properties readConfigFile(String filename)
    {
       	Properties config = new Properties();
	FileInputStream in = null;
	try 
	{
	    in = new FileInputStream(filename);
	    config.load(in);
	    in.close();
	}
	catch(IOException ex)
	{
	    System.out.println("Cannot read from config file: " + filename);
	}

	return config;
    }

    public void run()
    {
	
    }


    public static void main(String[] args)
    {
	if(args.length < 2)
	{	    
	    System.err.println("Usage: java ProxyServer <configfile> <port>");
	    return;
	}
	try 
	{
	    Integer.parseInt(args[1]);
	}
	catch (NumberFormatException e)
	{
	    System.err.println("<port> given is not a number.");
	}
	System.out.printlm("Starting Proxy Server on Port: " + args[1]);
	ServerSocket server = new ServerSocket(Integer.parseInt(args[1]));
	while(true)
	{
	    System.out.println("Waiting for client requests ...");
	    Socket client = server.accept();
	    
	    System.out.println("====================================");
	    System.out.println("Received Request from " + client.getInetAddress());
	    System.out.println("====================================");
	    ProxyServer proxyServer = new ProxyServer(args[0], client);
    }

}
