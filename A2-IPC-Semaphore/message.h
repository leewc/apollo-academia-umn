int init_q(int key);
int msgprintf(int q_id, char *fmt, ...);
int msgread(void *buf, int len);
int msgwrite(void *buf, int len, int q_id, int msg_type);
int removequeue(int q_id);

#define MESSAGE_PERMISSION 0600                                          
#define MAX_SIZE 4096

typedef struct{
     long message_type;  
     char message_text[1];
}MESSAGE; 
