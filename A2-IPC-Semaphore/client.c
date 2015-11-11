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

int main(int argc, char** argv)
{
     int server_id;
     int client_id;
     int key;
     MESSAGE *msg;
     msg = (MESSAGE*) malloc(sizeof(MESSAGE) + MAX_SIZE - 1);

     if(argc != 2)
     {
	  fprintf(stderr, "Usage: %s <key>\n", argv[0]);
	  return 1;
     }
     
     key = atoi(argv[1]);
     if((server_id = init_q(key)) == -1)
     {
	  perror("Failed to get Server Message Queue");
	  return 1;
     }

     // put a message in the queue to notify the server we are listening
     // null message since we just want to send the pid (saved in msg type over)
     printf("Client: PID: %i \n", getpid());
     printf("Client: Got server ID: %i, Sending Initial Message to server... \n", server_id);
     
     msgprintf(server_id, getpid(), "Hi from Client!"); //first msgtype here is who it's from, if who it's for then can't get origin
     printf("Client:\t Waiting for server response. \n");

     //wait for a reply (blocking read)
     int receive;
     if((receive = msgrcv(server_id, msg, RECEIVE_SZ, getpid(), 0)) < 0)
     {
	  perror("Message Receive Failed.");
	  return 1;
     }
     
     //We should get a reply with the new client queue
     printf("Client: Received Message from Server: %s\n", msg->message_text);
     printf("Client: Will rendezvous at given point: %ld\n", msg->message_type);

     if((client_id = init_q(msg->message_type)) == -1)
     {
	  perror("Failed to access server created client_q");
	  return 1;
     }
     
     printf("Client: Successfully connected to client Q of ID: %i ..\n", client_id);
     while(1) //same as for (;;)
     {
	  // CHECK IF THIS SHOULD BE GETPID OR JUST --- 0 shld be getpid
       if((receive = msgrcv(client_id, msg, RECEIVE_SZ, 0, 0)) < 0)
	  {
	       perror("Message Receive Failed.");
	       return 1;
	  }
	  printf("Client: Received Message from Server: %s\n", msg->message_text);
	  
	  msgprintf(client_id, server_id, "Thank you, shutting down.");
	  break; //let's just kill itself for now.
     }
     printf("Shutting down client.\n");
     removequeue(client_id);
     return 0;
}

