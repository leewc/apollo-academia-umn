package shared;

import java.io.Serializable;

import java.io.*;

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

	// public byte[] serializeAsCStruct(){
	// 	byte[] array = new byte[MsgT.BUFFER_SIZE + 16]; //4 + 4 + 4 + 4

	// 	array[0] = (byte) (this.msgType >> 24);
	// 	array[1] = (byte) (this.msgType >> 16);
	// 	array[2] = (byte) (this.msgType >> 8);
	// 	array[3] = (byte) (this.msgType);


	// 	array[4] = (byte) (this.cur_sequence >> 24);
	// 	array[5] = (byte) (this.cur_sequence >> 16);
	// 	array[6] = (byte) (this.cur_sequence >> 8);
	// 	array[7] = (byte) (this.cur_sequence);


	// 	array[8] = (byte) (this.max_sequence >> 24);
	// 	array[9] = (byte) (this.max_sequence >> 16);
	// 	array[10] = (byte) (this.max_sequence >> 8);
	// 	array[11] = (byte) (this.max_sequence);


	// 	array[12] = (byte) (this.payload_len >> 24);
	// 	array[13] = (byte) (this.payload_len >> 16);
	// 	array[14] = (byte) (this.payload_len >> 8);
	// 	array[15] = (byte) (this.payload_len);

	// 	//17th byte onwards
	// 	int index = 0;
	// 	for(int i = 16; i < array.length; i++)
	// 	{
	// 		array[i] = (byte) this.payload[index];
	// 		index++;
	// 	}

	// 	return array;
	// } 
	public int[] serializeAsCStruct(DataOutputStream ds) throws IOException
	{
		int[] array = new int[MsgT.BUFFER_SIZE]; //4 + 4 + 4 + 4

		// ds.write( (this.msgType >> 24));
		// ds.write( (this.msgType >> 16));
		// ds.write( (this.msgType >> 8));
		ds.write( (this.msgType));


		// ds.write( (this.cur_sequence >> 24));
		// ds.write(  (this.cur_sequence >> 16));
		// ds.write(  (this.cur_sequence >> 8));
		ds.write(  (this.cur_sequence));


		// ds.write(  (this.max_sequence >> 24));
		// ds.write(  (this.max_sequence >> 16));
		// ds.write(  (this.max_sequence >> 8));
		ds.write(  (this.max_sequence));


		// ds.write(  (this.payload_len >> 24));
		// ds.write(  (this.payload_len >> 16));
		// ds.write(  (this.payload_len >> 8));
		ds.write(  (this.payload_len));

		// 17th byte onwards
		// int index = 0;
		// for(int i = 16; i < array.length; i++)
		// {
		// 	array[i] = this.payload[index];
		// 	index++;
		// }

		// for(char c: payload)
		// 	if(c != '\0'){
		// 		System.out.println(c);
		// 		ds.write((int) c);
		// 	}
		String compile = new String(payload);
		System.out.println("DDD  " + compile);
		// byte[] bytes = compile.getBytes();
		for (char c : compile.toCharArray())
			ds.write(c);
		// ds.writeInt(array);
		ds.flush();
		return array;
	}
}