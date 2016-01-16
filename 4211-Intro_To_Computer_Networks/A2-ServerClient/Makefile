# Makefile adapted from: https://www.devin.com/cruft/javamakefile.html
JAVAC=javac
FLAGS= -cp . -g

# Begin define sources, this approach is used so we only compile changed .java files
# The JVM is slow to start up and feeding one file each time is inefficient
sources = $(wildcard *.java)
classes = $(sources:.java=.class)

client_src = $(wildcard client/*.java)
client_classes = $(client_src:.java=.class)

server_src = $(wildcard server/*.java)
server_classes = $(server_src:.java=.class)

shared_src = $(wildcard shared/*.java)
shared_classes = $(shared_src:.java=.class)
# End define sources
# Begin Targets
all:	$(classes) shared client server

clean :
	rm -Rf client/*.class
	rm -Rf server/*.class
	rm -Rf shared/*.class
	rm -Rf *.class

%.class : %.java
	$(JAVAC) $(FLAGS) $<

shared : $(shared_classes)

client : shared $(client_classes)

server : shared $(server_classes)
