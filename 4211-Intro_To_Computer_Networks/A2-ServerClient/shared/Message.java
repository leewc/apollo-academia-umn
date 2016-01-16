package shared;

import java.io.Serializable;

public class Message implements Serializable
{
	//Message container to send over the wire like a 'packet'
	public static final long serialVersionUID = 42L; //because that's the meaning of life.

	public int msgType;
	int cur_sequence;
	int max_sequence;
	int payload_len;
	char[] payload; //kept as a char array to simulate C, a req, hence the inefficient conversions

	public Message(int msgType, int cur_sequence, int max_sequence, int payload_len, char[] payload)
	{
		this.msgType = msgType;
		this.cur_sequence = cur_sequence;
		this.max_sequence = max_sequence;
		this.payload_len = payload_len;
		this.payload = payload;
	}

	//For GET/ERROR/ACK requests
	public Message(int msgType, char[] payload, int payload_len)
	{
		this.msgType = msgType;
		this.cur_sequence = 1;
		this.max_sequence = 1;
		this.payload_len = payload_len;
		this.payload = payload;
	}

	// Data is still transmitted as a char, so properly serialized.
	public char[] getPayload()
	{
		char[] data = new char[payload_len];
		for (int i = 0; i < payload_len; i++)
		{
			data[i] = this.payload[i];
		}
		assert(this.payload[payload_len] == '\0');
		return data;
	}

	public String getStatus()
	{
		StringBuilder status = new StringBuilder();
		status.append(this.msgType);
		status.append("-");
		status.append(MsgT.str_map[this.msgType]);
		status.append(" \t");
		status.append(this.cur_sequence);
		status.append(" \t");
		status.append(this.max_sequence);
		status.append("\t\t");
		status.append(this.payload_len);
		return status.toString();
	}
}