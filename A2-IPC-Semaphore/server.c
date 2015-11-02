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

#define MAXSIZE 4096

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
     printf("Server Initialized at Key Number: %i \n", key);
     printf("Waiting for clients. \n");

     int except = 0;
     while(1)
     {
	  int receive;
	  MESSAGE msg;
	  if((receive = msgrcv(self_id, &msg, MAXSIZE, except, MSG_EXCEPT)) < 0)
	  { //0 to indicate first message
	       perror("Message Receive Failed.");
	       return 1;
	  }
	  printf("Received message From Client of pid: %ld \n", msg.message_type);

	  //create a client_q using provided pid in message_type
	  int client_key = msg.message_type;
	  int client_id = init_client_q(client_key);
	  
	  printf("Initialized client key: %i id: %i \n", client_key, client_id);
	  //msgwrite("Server responding by putting message in main_q.", 47, client_id, client_key);
	  msgwrite("R.", 1, client_id, client_key);
	  
	  printf("Waiting for next client. \n");

	  msgwrite("Hi. Client.", 11, client_id, self_id); //selfid no matter here.
	  except = client_key;
     }

     printf("Shutting Down Server .. \n");
     removequeue(self_id);
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
     MESSAGE msg;
     msg.message_type = key;
     msg.message_text[0] = 'R'; //temporary.
     if(msgsnd(self_id, &msg, 1, 0) == -1)
     {
	  fprintf(stderr, "Failed to send reponse to client.");
	  return -1;
     }
     printf("Client Q initialized with id: %i \n", client_id);
     return client_id;
}
