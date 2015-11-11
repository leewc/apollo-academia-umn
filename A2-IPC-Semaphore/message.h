int init_q(int key);
int msgprintf(int q_id, int msg_type, int pid, char *fmt, ...);   /* Params: Q_ID, TO, FROM, MESSAGE */
int msgread(void *buf, int len);
int msgwrite(void *buf, int len, int q_id, int msg_type);
int removequeue(int q_id);

#define MESSAGE_PERMISSION 0600                                          
#define MAX_SIZE 4096

#define RECEIVE_SZ sizeof(MESSAGE) + MAX_SIZE - 1

typedef struct{
     long message_type;  // destination 
     long pid;           // origin (source)
     char message_text[1];
}MESSAGE; 
