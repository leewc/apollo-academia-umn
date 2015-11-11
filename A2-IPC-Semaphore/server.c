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
void receiveMessageFromClient(MESSAGE* msg, int receive); 

static int q_id; // the IPC message Queue ID
static int server_pid = 1; //Our 'pid' is set as 1 by default to distinguish messages for us, the server

int main(int argc, char** argv)
{
     if(argc != 2)
     {
	  fprintf(stderr, "Usage: %s <key>\n", argv[0]);
	  return 1;
     }
     
     int key = atoi(argv[1]);
     if((q_id = init_q(key)) == -1)
     {
	  perror("Failed to initialize Server Message Queue");
	  return 1;
     }
     printf("Server: PID: %i \n", getpid());
     printf("Server: Server Initialized at Key Number: %i \n", key);
     printf("Server: Waiting for clients to connect ... \n");

     while(1)
     {
	  MESSAGE *msg;
	  msg = (MESSAGE *) malloc(sizeof(MESSAGE) + MAX_SIZE -1 );
	  int receive = 0;

	  receiveMessageFromClient(msg, receive);
	  
	  msgprintf(q_id, msg->pid, server_pid, "Welcome client!"); //respond

	  receiveMessageFromClient(msg, receive);

	  msgprintf(q_id, msg->pid, server_pid, "Please shut down. Goodbye"); 
	  
	  printf("Server: Waiting for next client... \n");

	  free(msg);
	  //break; //kill ownself after one client for now
     }

     printf("Shutting Down Server ... \n");
     removequeue(q_id);
     return 0;
}

void receiveMessageFromClient(MESSAGE* msg, int receive)
{
     // receive messages of type 1 (which is our 'pid')
     if((receive = msgrcv(q_id, msg, RECEIVE_SZ, server_pid, 0)) < 0)
     {
	  perror("Message Receive Failed.");
     }
     printf("Server: Received message From Client: PID: %ld \n", msg->pid);
     printf("\t Message:  %s \n", msg->message_text); 	  
}

// function not used after change in requirements
int init_client_q(int key)
{
     int client_id;
     if((client_id = init_q(key)) == -1)
     {
	  fprintf(stderr, "Failed to initialize Client Message Queue: %i", key);
	  return -1;
     }
     //Notify client we are ready
     msgprintf(q_id, key, getpid(), "Please go to new Client Q."); 
     return client_id;
}
