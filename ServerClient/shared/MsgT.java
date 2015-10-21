package shared;
public class MsgT {
	// This is the enum class for MSG_TYPE_T
	public static final int MSG_TYPE_INVALID = 0;
	public static final int MSG_TYPE_GET = 1;
	public static final int MSG_TYPE_GET_ERR = 2;
	public static final int MSG_TYPE_GET_RESP = 3;
	public static final int MSG_TYPE_GET_ACK = 4;
	public static final int MSG_TYPE_FINISH  = 5;
	public static final int MSG_TYPE_MAX = 6;

	public static final int BUFFER_SIZE = 256;
	public static final Boolean DEBUG = true; // false suppresses additional terminal messages

	public static String[] str_map = {
	    "invalid",
	    "get",
	    "get_err",
	    "get_resp",
	    "get_ack",
	    "finish",
	    "max"
	};
}