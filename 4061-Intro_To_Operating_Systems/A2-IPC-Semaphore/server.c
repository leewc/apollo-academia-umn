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

/* includes for threading and semaphores */
#include <pthread.h>
#include <semaphore.h>

#include "message.h"

void receiveMessageFromClient(MESSAGE* msg, int receive); 
void *thread_execute(void *argv);

static int q_id; // the IPC message Queue ID
static int server_pid = 1; //Our 'pid' is set as 1 by default to distinguish messages for us, the server

int main(int argc, char** argv)
{
     sem_t semlock;
     pthread_t *tids;
     int i;
     int num_threads = 3;

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
     printf("Info: Initializing %i Threads ...\n", num_threads);
     printf("Info: [%i] Clients must connect before the server will shut down.\n", num_threads);  

     /* allocate and zero out memory for 3 threads */
     if((tids = (pthread_t *) calloc(num_threads, sizeof(pthread_t) ) ) == NULL)
     {
	  perror("Failed to allocate memory for thread IDs.");
	  return 1;
     }
     /* initialize semaphore with shared threads */
     if(sem_init(&semlock, 0, 1) < 0) /* 0 means shared among all threads, 1 means the initial semaphore value is set to 1. */
     {
	  perror("Failed to initialize Sempahores. \n");
	  return 1;
     }
     /* create threads and run execution function */
     for (i = 0; i < num_threads; i++)
     {
	  if(pthread_create(tids + i, NULL, thread_execute, &semlock)) //directly pass semlock as the args for the execute function
	  {
	       fprintf(stderr, "Failed to create thread : %i \n", i);
	       return 1;
	  }
     }
     /* Start Cleanup: Execution complete, join threads for result */
     for (i = 0; i < num_threads; i++)
     {
	  if(pthread_join(tids[i], NULL))
	  {
	       fprintf(stderr, "Failed to join thread : %i \n", i);
	       return 1;
	  }
     }

     printf("Info: All threads complete. Shutting Down Server ... \n");
     /* Destroy semaphore */
     sem_destroy(&semlock);
     removequeue(q_id);
     return 0;
}

/* function pointer that will send 2 messages and read 3 from the client. */
void *thread_execute(void *argv)
{
     sem_t *lock = (sem_t *) argv;
     printf("Server: (pthread ID %lu) has started. Waiting for client to connect ...\n", (unsigned long) pthread_self());

     while(1)
     {
	  MESSAGE *msg;
	  msg = (MESSAGE *) malloc(sizeof(MESSAGE) + MAX_SIZE -1 );
	  int receive = 0;
	  /* ----- ENTRY SECTION ----- */
	  while(sem_wait(lock) == -1)
	  {
	       if(errno != EINTR) //if interrupted
	       {
		    perror("Thread failed to lock semaphore");
		    return NULL;
	       }
	  }
	  /* ----- CRITICAL SECTION ----- */
	  printf("Server: (pthread ID: %lu) has the lock.\n", (unsigned long) pthread_self());
	  receiveMessageFromClient(msg, receive);
	  
	  msgprintf(q_id, msg->pid, server_pid, "Welcome client!"); //respond
	  
	  receiveMessageFromClient(msg, receive);
	  
	  msgprintf(q_id, msg->pid, server_pid, "OK that's enough. Please shut down. Goodbye.");
	  
	  receiveMessageFromClient(msg, receive);

	  /* ----- EXIT SECTION ----- */
	  if(sem_post(lock) == -1)
	  {
	       perror("Thread failed to unlock semaphore.\n");
	  }
	  free(msg);
	  break; //kill ownself after one client for now
     }
     printf("Server: Waiting for next client... \n");
     return NULL;
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
