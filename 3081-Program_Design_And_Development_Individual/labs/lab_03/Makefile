WordCount: readInput.o regex.o WordCount.o main.o
	g++ readInput.o regex.o WordCount.o main.o -o WordCount

runTests: regex.o WordCount.o WordCount_tests.h
	
	cxxtest/bin/cxxtestgen --error-printer --abort-on-fail --have-eh -o WordCount_tests.cpp WordCount_tests.h
	g++ -Wall -Icxxtest WordCount_tests.cpp regex.o WordCount.o -o WordCount_tests
	./WordCount_tests

clean: 
	rm -rf *o WordCount WordCount_tests 


#splitting up targets to only recompile if there are modifications made
main.o: main.cpp
	g++ -c main.cpp

WordCount.o: WordCount.cpp 
	     g++ -c WordCount.cpp 

regex.o: regex.cpp 
	 g++ -c regex.cpp

readInput.o: readInput.cpp
	     g++ -c readInput.cpp 


