FLAGS = -Wall -g

all: ls

ls.o: ls.c
	gcc $(FLAGS) ls.c -c

ls: ls.o
	gcc $(FLAGS) ls.o -o ls

clean:
	rm *.o
