// Shared functions for both client and server to output and write messages to the queue. 

#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <stdarg.h>
#include <stdlib.h>
#include <sys/ipc.h>
#include <sys/msg.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>

#include "message.h"

int init_q(int key)
{
     int q_id;
     q_id = msgget(key, IPC_CREAT | MESSAGE_PERMISSION);     
     if (q_id == -1)
     {
	  return -1;
     }
     return q_id;
}

int msgwrite(void *buf, int len, int q_id, int msg_type)
{
     int error = 0;
     MESSAGE *msg;
     if(( msg = (MESSAGE*) malloc(sizeof(MESSAGE) + len - 1)) == NULL)
     { /*len -1 because the struct has a byte for char already */
	  return -1;
     }
     memcpy(msg->message_text, buf, len);
     msg->message_type = msg_type;
     if(msgsnd(q_id, msg, sizeof(MESSAGE) + len - 1, 0) == -1)
	  error = errno;

     free(msg);
     if (error) 
     {
	  errno = error;
	  return -1;
     }
     return 0;     
}

int msgprintf(int q_id, int msg_type, int pid, char *fmt, ...) {               
     /* output a formatted message */
     va_list ap;
     char ch;
     int error = 0;
     int len;
     MESSAGE *msg;
 
     /* set up the format for output */
     va_start(ap, fmt);                       
     /* how long would it be ? */
     len = vsnprintf(&ch, 1, fmt, ap);              
     if ((msg = (MESSAGE *)malloc(sizeof(MESSAGE) + len - 1)) == NULL)
	  return -1;
     /* copy into the buffer */
     vsprintf(msg->message_text, fmt, ap);
     /* message type is who its for */    
     msg->message_type = msg_type;
     /* pid is used to keep track of origin */
     msg->pid = pid;
     if (msgsnd(q_id, msg, sizeof(MESSAGE) + len - 1, 0) == -1) 
	  error = errno;
     free(msg);
     if (error) {
	  errno = error;
	  return -1;
     }
     return 0;
}

int removequeue(int q_id) {
     return msgctl(q_id, IPC_RMID, NULL);
}
