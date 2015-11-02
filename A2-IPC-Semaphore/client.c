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

#define MAXSIZE 4096

int main(int argc, char** argv)
{
     int server_id;
     int client_id;
     int key;
     MESSAGE msg;

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
     printf("Self PID: %i \n", getpid());
     printf("Got server ID: %i, Sending Initial Message to server... \n", server_id);
     msgwrite("Hi from Client", 14, server_id, getpid());
     printf("Now waiting for server response. \n");


     //Sleep here to wait for client q init?

     //wait for a reply
     int receive;
     if((receive = msgrcv(server_id, &msg, 1, getpid(), 0)) < 0)
     {
	  perror("Message Receive Failed.");
	  return 1;
     }
     
     //We should get a reply with the new client queue
     printf("Received Text from Server Q: %s\n", msg.message_text);
     printf("This should be the rendezvous point: %ld\n", msg.message_type);

     if((client_id = init_q(msg.message_type)) == -1)
     {
	  perror("Failed to access server created client_q");
	  return 1;
     }
     
     printf("Successfully connected to client q of: %i ..\n", client_id);
     while(1) //same as for (;;)
     {
	  // CHECK IF THIS SHOULD BE GETPID OR JUST --- 0
	  if((receive = msgrcv(client_id, &msg, MAXSIZE, getpid(), 0)) < 0)
	  {
	       perror("Message Receive Failed.");
	       return 1;
	  }
	  printf("From Server: %s\n", msg.message_text);
	  //write some response here.
	  break; //let's just kill itself for now.
     }
     printf("Shutting down client.\n");
     return 0;
}

