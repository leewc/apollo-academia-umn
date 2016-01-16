# README.txt for minsh.c
# F2015 CSCI 4061 Assignment/Lab 1 : Shell
# Name : Wen Chuan Lee (leex7095)
#      : Mingchen Tang (tangx504)

# Introduction
This is a very basic shell with the ability to continually receive user
input, as well as call fork and exec on external commands. It also features
proper background process handling, and error handling from the child 
return signals. There is also clone functionality built in, some commands
which require sudo. The user will be notified if there is a failed clone 
due to lack of sudo.

# Building and running the shell
Simply run the basic Makefile to build the shell, the Makefile has a 
default goal that compiles minsh with all warning flags. Run 'make' to 
compile the shell.

Alternatively, compile the shell with 'gcc -Wall -g minsh.c -o minsh' or
without the flags.

After that just run the shell with './minsh'

# Basic Commands
  Command	Usage
  exit		terminate the shell session
  quit		terminate the shell session
  <command> &	ampersand [&] runs a process in the background, shell will not wait for child to finish execution

  clone		displays available clone options
  clone net	creates a new virtual network namespace, calls ip link to demonstrate (needs root)
  clone ns 	creates a new mount namespace (needs root)
  clone files	shares file descriptor table between parent (us) and child (subshell)
  clone fs	share file system information between parent and child
  clone io	shares IO context between parent and child
  clone vm	child and parent run in the same memory space

# What works and doesn't
  I believe everything works with ample testing and error handling, exiting
a subshell spawned by minsh will bring the control back to minsh. If 
CLONE_NEWPID was used i the clone calls, this will not happen as the child 
will hhave a new pid namespace. This is by design. 

# Who worked on this project
2 people as per listed on the top of this document. 

# Shell Design

As a shell needs to receive input and execute commands, design was started
with robust user input and argument parsing. Error handling was added 
(what if the user just hits enter with no input, bad input), getline was 
used instead of the usual suggested fgets to ensure there is no hard limit 
on input (and *paranoid* buffer overflows). 

Arguments were parsed initially with getInputWithoutDelimiter function, but
later decided to use the makeargv parse code provided in the course 
textbook. 

After which implementing exit and quit commands was done, this included
proper freeing of memory.

Fork and Execute was later added in, where aside from the built in command
'clone', 'quit', 'exit', execvp is called to run external programs. Wait is
then also included with the option to not wait using the ampersand(&) sign.

Finally clone was added in, in which clone net will first demonstrate that
the clone call worked using 'ip link', while the other clones spawn a 
proper subshell.

Most of the time was spend reading and understanding how to use the 
system calls with the help of man pages (mainly) and the internet as well 
as the textbook.
