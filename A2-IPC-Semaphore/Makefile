FLAGS = -Wall -g

message.o: message.h message.c
	gcc $(FLAGS) message.c -c
client: message.o
	gcc $(FLAGS) message.o client.c -o client
server: message.o
	gcc $(FLAGS) message.o server.c -o server

all: message.o client server

clean:
	rm message.o
	rm client
	rm server
