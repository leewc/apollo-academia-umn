import java.util.Properties;

import java.io.*;
import java.net.*;

import java.util.*;
/* Questions:
	- do we need to deal with http 1.0
	- do we forward other metadata such as mozilla
	- do we display ALL request headers
   Note: Putting this as one file for ease of compilation during submission
*/

public class ProxyServer extends Thread
{
    Properties config;
    Socket client;
    Socket server; //server we are contacting as the proxy

    BufferedReader in_client;
    OutputStream out_client;

    InputStream in_server;
    OutputStream out_server;

     /* Used to establish connection with the server */
    String host;
    int port;

    public ProxyServer(String configFilename, Socket client)
    {
    	this.config = readConfigFile(configFilename);
    	this.client = client;

	//System.out.println("HERE's the config file");
	//readConfigFile(configFilename).list(System.out);
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

    protected String readline(BufferedReader rdr) throws IOException
    {
		String line = "";
		if((line = rdr.readLine()) == null)
		{
		  throw new IOException("End of Buffer.");
		}
		return line;
    }

	protected Socket connectToServer() throws IOException
	{
		host = host.trim(); //remove any possible swhitespace left from the headers
		System.out.println("Connecting to " + host + " :" + port + " ...");
		Socket socket = new Socket(host, port);
		System.out.println("Connected.");

		// default charset
		in_server = socket.getInputStream();
		out_server = socket.getOutputStream();
		return socket;
	}

	private void shutdown() throws IOException
	{
		client.close();
		server.close();
	}

    public void run()
    {
    	try 
    	{
    		/* Using default charset on system */
    		in_client = new BufferedReader(new InputStreamReader(client.getInputStream()));
    		out_client = client.getOutputStream();

    		/* To hold header requests to be sent after validation */
    		StringBuilder header = new StringBuilder(1024);

	      	//ByteArrayOutputStream headerBuf = new ByteArrayOutputStream(8096);
			//PrintWriter headerWriter = new PrintWriter(headerBuf);

    		boolean notSupported = false;

    		String line; 	//holds a line of the header
    		String[] requestLine;

	      	String urlPath;
	      	URL resourceURL;

	      	line = readline(in_client);
	      	header.append(line);
	      	header.append("\n");

	      	// Request type
	      	requestLine = line.split(" "); //split by spaces
	      	if (requestLine[0].toUpperCase().equals("GET"))
	      	{
		   		System.out.println("GET");
		   		if(requestLine[1].toUpperCase().startsWith("HTTP"))
		   		{
		   			resourceURL = new URL(requestLine[1]);
		   			host = resourceURL.getHost();
		   			port = resourceURL.getPort();
		   			if (port == -1)
		   				port = 80;
		   			System.out.println("DEBUG: Request Method=GET " + resourceURL.toString());
		   		}
		   		else
		   		{
		   			notSupported = true;
		   		}
	      	}
	      	else if (requestLine[0].toUpperCase().equals("HEAD"))
	      	{
		  		System.out.println("DEBUG: Request Method HEAD");
	      	}
	      	else
	      	{
		   		notSupported = true;
		   		System.out.println("DEBUG: Unsupported Request Method " + requestLine[0]);
	      	}

	      	line = readline(in_client);
	      	header.append(line);
	      	header.append("\n");

	      	//HOST Header	      	
	      	requestLine = line.split(":");
	      	if (requestLine[0].toUpperCase().equals("HOST"))
	      	{
	      		host = requestLine[1];
	      		System.out.println("HOST IS ---2---" + host);	
	      		port = 80; 		//default to port 80 first
	      		if(requestLine.length == 3)
	      		{
	      			port = Integer.parseInt(requestLine[2]);
	      		}
	      		System.out.println("DEBUG: HOST " + host + " PORT: " + port);
	      	}
	      	else 
	      		throw new UnsupportedOperationException();

	      	if(notSupported){
	      		System.out.println("Killing not supported req");
	      		return;
		    }

	      	server = connectToServer();

	      	System.out.println("Writing header to server.");

	      	//read rest of the request
			while((line = in_client.readLine()) != null && line.length() != 0)
			{
				header.append(line);
				header.append("\n");
				System.out.println(line);
			}
			header.append("Connection:close\n\n");
			System.out.println("complete append. \n\n\n" + header.toString());
			out_server.write(header.toString().getBytes());

			System.out.println("Receiving data and writing to client.");

			byte response[] = new byte[8192];
			int count;
			while((count = in_server.read(response, 0, 8192)) > -1)
			{
				System.out.println(count);
				out_client.write(response, 0, count);
			}

	      	System.out.println("End.");
	      	shutdown();
		}
		catch (IOException e)
		{
			e.printStackTrace();
		}
	}


    public static void main(String[] args) throws IOException
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
	System.out.println("Starting Proxy Server on Port: " + args[1]);
	ServerSocket server = new ServerSocket(Integer.parseInt(args[1]));
	while(true)
	{
	    System.out.println("Waiting for client requests ...");
	    Socket client = server.accept();
	    
	    System.out.println("====================================");
	    System.out.println("Received Request from " + client.getInetAddress());
	    System.out.println("====================================");

	    ProxyServer proxyServer = new ProxyServer(args[0], client);
	    //start the thread.
	    proxyServer.start();
	}
    }

}
