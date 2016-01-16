# README.txt for minsh.c
# F2015 CSCI 4061 Assignment/Lab 2 : IPC with Message Queues/Semaphores and Threading
# Name : Wen Chuan Lee (leex7095)
#      : Mingchen Tang (tangx504)

# Introduction

This is a client/server process that communicates through System V Message Queues on Linux. Message structures are passed between processes for Inter Process Communication (IPC). Additional server threads are created that will read the queue. POSIX Semaphores are used to ensure each thread reads the queue only when no other threads are reading it to avoid race conditions.

# Executing the Client and Server 

1. Run make in the directory where the Makefile is located to build the executables
2. First start the server by typing: 
		./server 9876     (9876 is the key for the Queue)
3. In another terminal, start a client by typing: 
		./client.c 9876   (key for client must identical to the key passed into the server)
4. The client will send 3 messages in total and receive 2 from the server. The shutdown.
5. Start a few more clients for the other threads in the IPC. Once each thread has a client, the server will shutdown and delete the queue.
6. Printed messages are shown in the command line at each step of the process.

Note: The default number of threads is 3 (thus 3 clients must be started before the server will shutdown and remove the queue.
(This can be changed by updating the value of num_threads in server.c)

# What Works and Doesn't
Everything works as it should. The queue should not exist with any messages when the server is started, so the server can properly initialize the queue and wait for messages from the client.

# Design

The IPC part of the assignment was set up first. By ensuring a single threaded server process and client can correctly communicate, we can introduce threads later with the use of semaphores. As multithreaded programming is a common headache, it is important to ensure that the underlying single threaded implementation actually works before implementing threads. 

Both client and server processes communicate from 1 SystemV IPC Queue. Initially a separate client queue was set up, but communication can be simplified by changing the message structure, and having only one main queue. 

In a message structure, message_type will be the 'destination' (which process the message is for), and then message_text is the payload (the messages), an additional pid variable is used to keep track of the 'origin' (who it's from). Servers will read messages with type 1 (1 means it is meant for the server) and clients will read messages that have a message_type equal to their PID. This avoids the need to delicately send and receive from both sides. Initially the server and client orchastrate each send/receive without the extra PID field.

Reads are blocking while writes are not in the Message Queue implemetnation. This is then extended in other threads that we minimize critical sections to avoid total blocking. Semaphores dictate which thread can read/write (communicate) with the client process, before releasing the semaphore flag and passing the 'lock' to someone else.

Unnamed POSIX semaphores <semaphore.h> are used instead of the older SystemV semaphores <sys/sem.h> as there is cleaner implementation, and that they are newer and more robust.

We have referred to the man pages and resources like StackOverflow for solving some issues. The most helpful resource would be the slides (for functions to use) and the book for properly implementing semaphores, threads and message queues.

# Outputs

Outputs for ./server and ./client are provided in server_output.txt and client_output.txt.