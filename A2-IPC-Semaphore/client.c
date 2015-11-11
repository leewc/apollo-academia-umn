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

/* Client will send 3 messages in total and wait to receive 2 messages, then shutsdown. */
int main(int argc, char** argv)
{
     int server_qid;
     int client_pid = getpid(); /* our own pid */
     int key;
     MESSAGE *msg;
     msg = (MESSAGE*) malloc(sizeof(MESSAGE) + MAX_SIZE - 1);

     if(argc != 2)
     {
	  fprintf(stderr, "Usage: %s <key>\n", argv[0]);
	  return 1;
     }
     
     //obtain the server through a common key.
     key = atoi(argv[1]);
     if((server_qid = init_q(key)) == -1)
     {
	  perror("Failed to get Server Message Queue");
	  return 1;
     }

     printf("Client: PID: %i \n", client_pid);
     printf("Client: Connected to Server Queue ID: %i ...\nSending Initial Message to server... \n", server_qid);
     
     // put a message in the queue to notify the server we are listening
     msgprintf(server_qid, 1, client_pid, "Hi from Client!"); 
     printf("Client: Waiting for server response. \n");

     //wait for a reply (blocking read)
     int receive;
     if((receive = msgrcv(server_qid, msg, RECEIVE_SZ, client_pid, 0)) < 0)
     {
	  perror("Message Receive Failed.");
	  return 1;
     }
     
     //We should get a reply.
     printf("Client: Received Message from Server:\n\t%s\n", msg->message_text);

     while(1) //same as for (;;)
     {
       printf("Client: Sending Reply.. \n");
       msgprintf(server_qid, 1, client_pid, "Send me something!");
       if((receive = msgrcv(server_qid, msg, RECEIVE_SZ, client_pid , 0)) < 0)
	  {
	       perror("Message Receive Failed.");
	       return 1;
	  }
	  printf("Client: Received Message from Server:\n\t%s\n", msg->message_text);
	  
	  msgprintf(server_qid, 1, client_pid, "Thank you, shutting down.");
	  break; //client shuts down after receiving 2 messages. 
     }
     printf("Client: Shutting down client.\n");
     return 0;
}
