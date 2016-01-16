# Makefile adapted from: https://www.devin.com/cruft/javamakefile.html
JAVAC=javac
FLAGS= -cp . -g -Xlint

# Begin define sources, this approach is used so we only compile changed .java files
# The JVM is slow to start up and feeding one file each time is inefficient
sources = $(wildcard *.java)
classes = $(sources:.java=.class)

# End define sources
# Begin Targets
all:	$(classes)

clean :
	rm -Rf *.class

%.class : %.java
	$(JAVAC) $(FLAGS) $<
