import java.io.*;
import java.net.*;

import java.util.*;
/* Questions:
	- do we forward other metadata such as mozilla/cookies (think so)
	- do we need to post
	- do we need to deal with http 1.0
	- do we just respond with status code
	- do we display ALL request headers
	- do we always close the stream
	- do we need a timeout
	- microsoft.com has useragent string bot message
	- theverge doesn't respond somehow
   Note: Putting this as one file for ease of compilation during submission
*/

/* Simple HTTP 1.1 proxy server that supports blacklist and GET, HEAD requests */
public class ProxyServer extends Thread
{
    Validator validator;
    Socket client;
    Socket server; //server we are contacting as the proxy

    BufferedReader in_client;
    OutputStream out_client;

    BufferedInputStream in_server;
    OutputStream out_server;

     /* Used to establish connection with the server */
    String host;
    int port;

    /* To hold header requests to be sent after validation */
    StringBuilder header;

    /* Constructor called when a client connection is made */
    public ProxyServer(Socket client, Validator validator) throws IOException
    {
    	this.client = client;
    	this.validator = validator;

    	/* Using default charset on system */
    	in_client = new BufferedReader(new InputStreamReader(client.getInputStream()));
    	out_client = client.getOutputStream();

   		header = new StringBuilder(4096);
   	}

    /* 
       Returns a string that is read and also appends to the header string
    */
    protected String readline(BufferedReader rdr) throws IOException
    {
		String line = "";
		if((line = rdr.readLine()) == null)
		{
		  throw new IOException("End of Buffer.");
		}
		return line;
    }

    protected void addToHeader(String line)
    {
    	header.append(line);
		header.append("\n"); //readLine consumes newlines
    }

	protected Socket connectToServer() throws IOException
	{
		System.out.println("Connecting to " + host + " :" + port + " ...");
		Socket socket = new Socket(host, port);
		System.out.println("Connected.");

		socket.setSoTimeout(10000);
		// default charset
		in_server = new BufferedInputStream(socket.getInputStream());
		out_server = socket.getOutputStream();
		return socket;
	}

	protected void getAndSetHost(String[] requestLine)
	{
		if (validator.hasHost(requestLine[0]))
	    {
      		host = requestLine[1].trim();
      		port = 80; 		//default to port 80 first
      		if(requestLine.length == 3)
      			port = Integer.parseInt(requestLine[2]);
      		
      		System.out.println("DEBUG: HOST " + host + " PORT: " + port);
	    }
	    else 
	      	throw new RuntimeException("No valid HOST found in header");
	}

	protected void send(byte[] resp) throws IOException
	{
		out_client.write(validator.resp_header);
		out_client.write(resp);
		out_client.write(validator.CLRF);
	}

	private void shutdown() throws IOException
	{
		client.close();
		if(server != null)
			server.close();
	}

    public void run()
    {
    	try 
    	{
    		String[] requestLine;
	      	String line = new String("");
    		URL resourceURL;

	      	// Request type
	      	line = readline(in_client);
	      	requestLine = line.split(" "); //split by spaces
      	 	if (( validator.isGet(requestLine[0]) || validator.isHead(requestLine[0]) ) 
	      			&& validator.isHTTP(requestLine[1]) )
	      	{
	      		addToHeader(line);
		   		resourceURL = new URL(requestLine[1]);
		   		host = resourceURL.getHost().trim(); //remove whitespace left by split
		   		port = resourceURL.getPort();
		   		if (port == -1)
		   			port = 80;
		   		System.out.println("DEBUG: Request Method=" +requestLine[0] + " " + resourceURL.toString());
		  	}
		  	else
		  	{
	      		System.out.println("DEBUG: Unsupported Request Method " + requestLine[0]);
		   		send(validator.resp_notAcceptable);
		   		System.out.println("Killing.");
		   		shutdown();
		   		return;
		   	}

	      	//HOST Header
	      	line = readline(in_client);
	      	addToHeader(line);
	      	getAndSetHost(line.split(":"));

	      	server = connectToServer();


	      	//read rest of the request
			while((line = in_client.readLine()) != null && line.length() != 0)
			{
				addToHeader(line);
				System.out.println(line);
			}

			if(header.toString().startsWith("GET"))
			{
				header.append("Connection: close\n\r\n");	
			}
			else
				header.append("\r\n");
			
			System.out.println("REQUEST HEADER SIZE: " + header.toString().length());
	      	System.out.println("Writing header to server.");

			out_server.write(header.toString().getBytes());

			System.out.println("Receiving data and writing to client.");

			byte response[] = new byte[8192];
			int count;

			try
			{
				while((count = in_server.read(response, 0, 8192)) > -1)
				{
					System.out.println(count);
					out_client.write(response, 0, count);
				}
			}
			catch(SocketTimeoutException e)
			{
				System.out.println("Hmm. Timeout.");
				send(validator.resp_timeout);
			}
			System.out.println("Thread finished.");
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

		Validator validator = new Validator(args[0]);
		System.out.println("Starting Proxy Server on Port: " + args[1]);
		ServerSocket server = new ServerSocket(Integer.parseInt(args[1]));
		
		System.out.println("");
		while(true)
		{
		    System.out.println("Waiting for client requests ...");
		    Socket client = server.accept();
		    
		    System.out.println("====================================");
		    System.out.println("Received Request from " + client.getInetAddress());
		    System.out.println("====================================");

		    //pass the same instance of validator to thread.
		    ProxyServer proxyServer = new ProxyServer(client, validator);
		    //start the thread.
		    proxyServer.start();
		}
    }

}