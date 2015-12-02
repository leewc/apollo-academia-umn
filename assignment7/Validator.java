/* Only one public class in Java, this is a package-private (protected) one. */
/* Initially all in one file, split for cleaner code */
/* Need only one instance. */

import java.util.Properties;
import java.util.HashSet; //HashSet is not thread safe if modified, but for reads it is fine.
import java.util.Arrays;
import java.io.*;

class Validator
{
	private Properties config;
	public final byte[] resp_notAcceptable = "406 Not Acceptable\n".getBytes();
	public final byte[] resp_forbidden = "403 Forbidden\n".getBytes();
	public final byte[] resp_timeout = "408 Request Timeout\n".getBytes();
	public final byte[] resp_header = "HTTP/1.1 ".getBytes(); //notice the extra space, that's important
	public final byte[] CLRF = "\r\n".getBytes();

	public final HashSet<String> hopByHopHeaders = new HashSet<String>(Arrays.asList("connection", "keep-alive"));

	public Validator(String configFilename)
	{
		System.out.println("Loading config file : " + configFilename);
		config = readConfigFile(configFilename);
		System.out.println("Config file loaded.");
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

    /* Convenience methods for all supported Requests */
    public Boolean isGet(String string)
    {
    	return string.toUpperCase().equals("GET");
    }

    public Boolean isHTTP(String string)
    {
    	return string.toUpperCase().startsWith("HTTP");
    }

    public Boolean isHead(String string)
    {
    	return string.toUpperCase().equals("HEAD");
    }

    public Boolean hasHost(String string)
    {
    	return string.toUpperCase().equals("HOST");
    }

    public Boolean hostInBlackList(String host)
    {
    	System.out.println(host);
    	//sometimes the host does not have www
    	return (config.containsKey(host.toLowerCase()) || config.containsKey("www." + host.toLowerCase()));
    }

    /* Method should never have to check for null since we check if host is in blacklist first 
		If empty string returned or asterisk (*), every resource is blocked.
     */

    public Boolean resourceBlocked(String host, String contentType)
    {
    	System.out.println("checking block  :" + contentType);
    	String blockedType = config.getProperty(host.toLowerCase());
    	System.out.println("BLOCKED TYPE");
    	if(blockedType.equals("") || blockedType.equals("*"))
    		return true;
    	else if(blockedType.equals(contentType.toLowerCase()))
    		return true;
    	else
    		return false;
    }

    public Boolean isHopByHopHeader(String header)
    {
    	return hopByHopHeaders.contains(header.toLowerCase());
    }
}