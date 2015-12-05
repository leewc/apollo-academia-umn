import java.io.*;
import java.net.*;

import java.util.*;
// above imports include the Logger. Note: All logging methods are thread safe.
// ref: http://docs.oracle.com/javase/7/docs/api/java/util/logging/Logger.html

/* Simple HTTP 1.1 proxy server that supports blacklist and GET, HEAD requests. No POST, per assignment. */
public class ProxyServer extends Thread
{
    Validator validator;
    Socket client;
    Socket server; //server we are contacting as the proxy

    BufferedInputStream in_client;
    OutputStream out_client;

    BufferedInputStream in_server;
    OutputStream out_server;

     /* Used to establish connection with the server */
    String host;
    int port;

    /* To hold header requests/responses to be sent after validation */
    StringBuilder req_header;
    StringBuilder resp_header;

    /* Constructor called when a client connection is made */
    public ProxyServer(Socket client, Validator validator) throws IOException
    {
    	this.client = client;
    	this.validator = validator;

    	/* Using default charset on system */
    	in_client = new BufferedInputStream(client.getInputStream());
    	out_client = client.getOutputStream();

    	req_header = new StringBuilder(4096);
    	resp_header = new StringBuilder(4096);
   	}

    /* 
       Returns a string that is read and also appends to the header string
       Enforces we MUST have a line, if we have null throw the exception and force die.
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

    /* Reads the entire header fully first - then lets copies be made. */
    protected BufferedReader readHeaders(InputStream in, ByteArrayOutputStream hdr) throws IOException
    {
    	byte[] buffer = new byte[1024];
    	int len;
    	while ((len = in.read(buffer)) > -1 )
    	{
    		boolean found_CLRF = false;
    		hdr.write(buffer, 0, len);
    		for(int i=0; i <= buffer.length -4 ; i ++)
    		{
    			//13 for CR, 10 for LF
    			if(buffer[i] == (byte) 13 && buffer[i+1] == (byte) 10 
    				&& buffer[i+2] == (byte) 13 && buffer[i+3] == (byte) 10)
    				{
    					found_CLRF = true;
    					break; //stop for loop
    				}
    		}
    		if(found_CLRF)
    			break; //stop while loop
    	}
    	hdr.flush();

    	//return a ready to use BufferedReader (of default charset)
    	return new BufferedReader(new InputStreamReader(
    								new ByteArrayInputStream(hdr.toByteArray())));
    } 

    protected void addToHeader(String line, StringBuilder header)
    {
    	header.append(line);
		header.append("\n"); //readLine consumes newlines
    }

	protected Socket connectToServer() throws IOException
	{
		Socket socket = new Socket(host, port);
		System.out.println("Connected to " + host + " :" + port + " ...");

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
	    }
	    else if(host.length() == 0)
	    		throw new RuntimeException("No valid HOST found in header or request URL");
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
    		ByteArrayOutputStream requestHeader = new ByteArrayOutputStream(); //to make a copy of headers
   		
    		BufferedReader in_client_rdr = readHeaders(in_client, requestHeader); //to get original headers
    		if(processAndSendRequest(in_client_rdr) == false)
    		{
    			shutdown();
    			return;
    		}

			System.out.println("Receiving data and writing to client.");

			
			ByteArrayOutputStream responseHeader = new ByteArrayOutputStream(); //stores the response

			BufferedReader in_server_rdr = readHeaders(in_server, responseHeader); //gets the original header
			String TEST = new String(responseHeader.toByteArray());
			System.out.println("UNTOUCHED |||||||||||||||||| \n\n" + TEST);
			//out_client.write(responseHeader.toByteArray());
			if(processAndReceive(in_server_rdr) == false)
			{
				shutdown();
				return;
			}

			System.out.println("Thread finished.");
	      	shutdown();
		}
		catch (IOException e)
		{
			e.printStackTrace();
		}
	}

	protected boolean processAndSendRequest(BufferedReader in_client_rdr) throws IOException
	{
			String[] requestLine;
	      	String line = new String("");
    		URL resourceURL;
    		boolean isOnBlackList = false;

	      	// Request type
	      	line = readline(in_client_rdr);
	      	requestLine = line.split(" "); //split by spaces
      	 	if (( validator.isGet(requestLine[0]) || validator.isHead(requestLine[0]) ) 
	      			&& validator.isHTTP(requestLine[1]) )
	      	{
	      		addToHeader(line, req_header);
		   		resourceURL = new URL(requestLine[1]);
		   		host = resourceURL.getHost().trim(); //remove whitespace left by split
		   		port = resourceURL.getPort();
		   		if (port == -1)
		   			port = 80;
		   		System.out.println("DEBUG: Request Method=" +requestLine[0] +" HOST " + host);
		  	}
		  	else
		  	{
	      		System.out.println("DEBUG: Unsupported Request Method " + requestLine[0]);
		   		send(validator.resp_notAcceptable);
		   		return false;
		   	}

	      	//HOST Header
	      	if ( (line = in_client_rdr.readLine() ) != null)
	      	{
	      		addToHeader(line, req_header);
		      	getAndSetHost(line.split(":"));
	      	}

	      	//Check Blacklist
	      	if(validator.hostInBlackList(host))
	      	{
	      		isOnBlackList = true;
	      		if(validator.isCompletelyBlocked(host))
	      		{
	      			System.out.println("Site completely BLOCKED");
	      			send(validator.resp_forbidden);
	      			out_client.write("Sorry. This website is blocked.".getBytes());
	      			return false;
	      		}
	      	}

	      	server = connectToServer();

	      	//read rest of the request
			while((line = in_client_rdr.readLine()) != null && line.length() != 0)
			{
				if (!(validator.isHopByHopHeader(line) ))
				{
					if(!(isOnBlackList && validator.isBlockedType(line, host)))
						addToHeader(line, req_header);
					else
					{
						System.out.println("RESOURCE BLOCKED" + line);
		      			send(validator.resp_forbidden);
		      			out_client.write("Resource is blocked.".getBytes());
		      			return false;
					}
				}
			}

			if(req_header.toString().startsWith("GET"))
			{
				req_header.append("Connection: close\n\r\n");	
			}
			else
				req_header.append("\r\n");
			
			System.out.println("Writing header to server.");

			out_server.write(req_header.toString().getBytes());
			return true;
	}

	protected boolean processAndReceive(BufferedReader in_server_rdr) throws IOException
	{
		boolean isOnBlackList = false;
		if(validator.hostInBlackList(host))
		{
      		isOnBlackList = true;
      		if(validator.isCompletelyBlocked(host))
      		{
      			System.out.println("Site completely BLOCKED");
      			send(validator.resp_forbidden);
      			out_client.write("Sorry. This website is blocked.".getBytes());
      			return false;
      		}
	    }

	    //process the response header
	    String line = new String("");
		while((line = in_server_rdr.readLine()) != null && line.length() != 0)
		{
			// if (!(validator.isHopByHopHeader(line) ))
			// {
				if(!(isOnBlackList && validator.isBlockedType(line, host)))
					addToHeader(line, resp_header);
				else
				{
					System.out.println("RESOURCE BLOCKED" + line);
	      			send(validator.resp_forbidden);
	      			out_client.write("Resource is blocked.".getBytes());
	      			return false;
				}
			// }
			// else
			// {
			// 	System.out.println("HBH " + line);
			// 	throw new RuntimeException();
			// }
		}
		
		//must send the response headers

		System.out.println("RESP HEADER ||||||||||||||||||||||||||| \n\n " + resp_header.toString());

		out_client.write(resp_header.toString().getBytes());
		out_client.write(validator.CLRF);

		byte response[] = new byte[8192];
			int count;

			try
			{
				while((count = in_server.read(response, 0, 8192)) > -1)
				{
					//System.out.println(count);
					out_client.write(response, 0, count);
				}
			}
			catch(SocketTimeoutException e)
			{
				System.out.println("Hmm. Timeout.");
				send(validator.resp_timeout);
			}
			return true;

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

		    //pass the same instance of validator to each thread.
		    ProxyServer proxyServer = new ProxyServer(client, validator);
		    //start the thread.
		    proxyServer.start();
		}
    }

}