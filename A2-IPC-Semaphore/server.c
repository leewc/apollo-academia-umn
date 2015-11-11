#define _GNU_SOURCE

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

static int self_id;

int init_client_q(int key);

int main(int argc, char** argv)
{
     if(argc != 2)
     {
	  fprintf(stderr, "Usage: %s <key>\n", argv[0]);
	  return 1;
     }
     
     int key = atoi(argv[1]);
     if((self_id = init_q(key)) == -1)
     {
	  perror("Failed to initialize Server Message Queue");
	  return 1;
     }
     printf("Server: PID: %i \n", getpid());
     printf("Server: Server Initialized at Key Number: %i \n", key);
     printf("Server: Waiting for clients to connect ... \n");

     //necessary to avoid reading a just sent message (no semaphores implemented yet)
     int except = 0;
     while(1)
     {
	  int receive;
	  MESSAGE *msg;
	  msg = (MESSAGE *) malloc(sizeof(MESSAGE) + MAX_SIZE -1 );
	  if((receive = msgrcv(self_id, msg, RECEIVE_SZ, except, MSG_EXCEPT)) < 0)
	  { //0 to indicate first message
	       perror("Message Receive Failed.");
	       return 1;
	  }
	  printf("Server: Received message From Client of pid: %ld \n", msg->message_type);
	  printf("\t Message is: %s \n", msg->message_text); 

	  //create a client_q using provided pid in message_type, this also creates a message in the main queue
	  int client_key = msg->message_type;
	  int client_id = init_client_q(client_key);
	  
	  printf("Server: Initialized Client Q with ID: %i Key: %i  \n", client_id, client_key);
	  
	  //Respond by putting message in client_q;
	  msgprintf(client_id, client_key, "Welcome client, this is your client Q!");

	  //Get a response from the client_q, through client_key
	  if((receive = msgrcv(client_id, msg, RECEIVE_SZ, self_id, 0)) < 0)
	  {
	       printf("Response Error.\n");
	       return 1;
	  }
	  printf("Server: \t Message from Client: %s \n", msg->message_text); 
	  
	  //printf("Server: Waiting for next client. \n");

	  except = client_key;
	  free(msg);
	  break; //kill ownself after one client for now
     }

     printf("Shutting Down Server ... \n");
     removequeue(self_id);
     return 0;
}

int init_client_q(int key)
{
     int client_id;
     if((client_id = init_q(key)) == -1)
     {
	  fprintf(stderr, "Failed to initialize Client Message Queue: %i", key);
	  return -1;
     }
     //Notify client we are ready

     msgprintf(self_id, key, "Please go to new Client Q."); 
     return client_id;
}
