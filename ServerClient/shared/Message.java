package shared;

import java.io.Serializable;

public class Message implements Serializable
{
	//Message container to send over the wire like a 'packet'
	public static final long serialVersionUID = 42L;

	int msgType;
	int cur_sequence;
	int max_sequence;
	int payload_len;
	char[] payload;

	public Message(int msgType, int cur_sequence, int max_sequence, int payload_len, char[] payload)
	{
		this.msgType = msgType;
		this.cur_sequence = cur_sequence;
		this.max_sequence = max_sequence;
		this.payload_len = payload_len;
		this.payload = payload;
	}

	//For GET requests
	public Message(int msgType, char[] payload, int payload_len)
	{
		this.msgType = msgType;
		this.cur_sequence = 1;
		this.max_sequence = 1;
		this.payload_len = this.payload_len;
		this.payload = payload;
	}

	public char[] getPayload()
	{
		return this.payload;
	}

	public String getStatus()
	{
		StringBuilder status = new StringBuilder();
		status.append(this.msgType);
		status.append(" ");
		status.append(MsgT.str_map[this.msgType]); //Check if we want the text or value
		status.append(" ");
		status.append(this.cur_sequence);
		status.append(" ");
		status.append(this.max_sequence);
		status.append(" ");
		status.append(this.payload_len);
		return status.toString();
	}
}