int init_q(int key);
int msgprintf(int q_id, int msg_type, char *fmt, ...);
int msgread(void *buf, int len);
int msgwrite(void *buf, int len, int q_id, int msg_type);
int removequeue(int q_id);

#define MESSAGE_PERMISSION 0600                                          
#define MAX_SIZE 4096

typedef struct{
     long message_type;  // destination 
     long pid;           // origin
     char message_text[1];
}MESSAGE; 

#define RECEIVE_SZ sizeof(MESSAGE) + MAX_SIZE - 1
