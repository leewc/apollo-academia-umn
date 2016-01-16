FLAGS = -Wall -g

all: client server

client.o: client.c
	gcc $(FLAGS) client.c -c

server.o: server.c
	gcc $(FLAGS) -pthread server.c -c

message.o: message.h message.c
	gcc $(FLAGS) message.c -c

client: message.o client.o
	gcc $(FLAGS) message.o client.o -o client
server: message.o server.o
	gcc $(FLAGS) -pthread message.o server.o -o server

clean:
	rm *.o
	rm client
	rm server
