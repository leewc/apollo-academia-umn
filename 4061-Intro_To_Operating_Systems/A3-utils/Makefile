FLAGS = -Wall -g

all: ls find grep

ls.o: ls.c
	gcc $(FLAGS) ls.c -c

ls: ls.o
	gcc $(FLAGS) ls.o -o ls

find.o: find.c
	gcc $(FLAGS) find.c -c

find: find.o
	gcc $(FLAGS) find.o -o find

grep.o: grep.c
	gcc $(FLAGS) grep.c -c 

grep: grep.o
	gcc $(FLAGS) grep.o -o grep

clean:
	rm ls
	rm find
	rm grep
	rm *.o
