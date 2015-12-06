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

	//put these here so they are compiled away. (for performance!)
	public final HashSet<String> hopByHopHeaders 
		= new HashSet<String>(Arrays.asList("connection", "keep-alive",
											"proxy-authenticate", "proxy-authorization",
											"te", "trailers", "transfer-encoding", "upgrade" ));

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
    	//sometimes the host does not have www
    	return (config.containsKey(host.toLowerCase()) || config.containsKey("www." + host.toLowerCase()));
    }

    /* Since host might not have www, this method tries both as keys to get the value */
    /* Should never return null since we check for membership in hostInBlackList */
    /* Strips off any asterisks for matching */
    public String getValueFromBlackList(String key)
    {
    	String value = config.getProperty(key.toLowerCase());
    	if(value == null)
    		value = config.getProperty("www." + key.toLowerCase());	
    	return value.replaceAll("\\*", ""); //escape
    }

    /* If empty string returned or asterisk (*), every resource is blocked. */
    public Boolean isCompletelyBlocked(String host)
    {
    	String blockedType = getValueFromBlackList(host);
    	return blockedType.equals("") || blockedType.equals("*");
    }

    public Boolean isHopByHopHeader(String header)
    {
    	return hopByHopHeaders.contains(header.split(":")[0].trim().toLowerCase());
    }

    /* Method should never have to check for null since we check if host is in blacklist first 
    	No need to check if totally blocked as this is handled by isCompletelyBlocked
     */
    public Boolean isBlockedType(String line, String host)
    {
    	String field = line.split(":")[0].trim().toLowerCase();
    	if (field.equals("accept") || field.equals("content-type")) //ref 14.1 and 14.17
    	{
    		String values = line.split(":")[1];
    		//for each value if matches type, return true (blocked) else false
    		//for(String value : values.split(";"))
    		//{
    			if(values.trim().toLowerCase().contains(getValueFromBlackList(host)))
    			{
    				System.out.println("isBlockedType   " + values);
    				return true;
    			}
    		//}
    	}
    	return false; //not a blocked type
    }

    // Function not used as we can check for presence of content-length
    public Boolean isChunked(String line) 
    {
    	if(line.toLowerCase().contains("chunked"))
    		return true;
    	return false;
    }

    public Integer tryGetContentLength(String line)
    {
    	String[] field_value = line.split(":");
    	if (field_value[0].trim().toLowerCase().equals("content-length"))
    	{
    		return Integer.parseInt(field_value[1].trim());
    	}

    	return null; //not the field we want
    }
}