int init_q(int key);
int msgprintf(char *fmt, ...);
int msgread(void *buf, int len);
int msgwrite(void *buf, int len, int q_id);
int msgwriteType(void *buf, int len, int q_id, int msg_type);
int removequeue(void);

#define MESSAGE_PERMISSION 0600                                                                                                                       
                                                                                                                                                    
typedef struct{
     long message_type;  
     char message_text[1];
}MESSAGE; 
