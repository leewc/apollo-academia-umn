FLAGS = -Wall -g

all: ls find

ls.o: ls.c
	gcc $(FLAGS) ls.c -c

ls: ls.o
	gcc $(FLAGS) ls.o -o ls

find.o: find.c
	gcc $(FLAGS) find.c -c

find: find.o
	gcc $(FLAGS) find.o -o find

clean:
	rm *.o
