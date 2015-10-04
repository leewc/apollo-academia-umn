#define _GNU_SOURCE
#define DELIMITERS " \n" //space, newlines are delimiters
#define STACK_SIZE (1024 * 1024) //Taken from example in man page

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/wait.h>
#include <unistd.h>
#include <sched.h>

void shell_loop();
int getInputWithoutDelimiter(char** input);
int makeargv(const char *s, const char *delimiters, char ***argvp);
int forkAndExecute(char** argvp, int waitForProcess); 
int cloneInterface(int interface);

int main(int argc, char *argv[])
{
  printf("Welcome to minsh. \n");
  shell_loop();
  return 0;
}

/*
  Starts the shell prompt to wait for user input and loop until an EOF or exit
  command is given, passes commands to other functions for handling.

  Adapted: 
  http://stackoverflow.com/questions/7831755/what-is-the-simplest-way-of-getting-user-input-in-c
  http://stackoverflow.com/questions/1247989/how-do-you-allow-spaces-to-be-entered-using-scanf
  Avoids buffer overflow by using fgets, or just use the built in getline (no new line this way)
  http://stackoverflow.com/questions/1252132/difference-between-scanf-and-fgets
  http://man7.org/linux/man-pages/man3/getline.3.html
*/

void shell_loop()
{
  int run = 1;
  while(run)
  {
    printf("--$ ");

    char** argvp;
    char *input = NULL;
    size_t buf_len = 0;
    ssize_t numchars = getline(&input, &buf_len, stdin);

    if(numchars == -1)
    {
      fprintf(stderr, "Failed to read input. \n");
    }

    int argvSize = makeargv(input, DELIMITERS, &argvp);

    // Prevent Segfault if user only hits enter
    if(argvSize < 1)
    {
      free(input);
      free(argvp);
      continue; // restart
    }

    /* ---- Begin Body of Process Control ---- */
    if(strcmp(argvp[0],"exit") == 0 || strcmp(argvp[0],"quit") == 0)
    {
      run = 0;
      continue;
    }
    else if(strcmp(argvp[0], "clone") == 0)
    {
	 if(argvSize == 1)
	 {
	      printf("Please specify additional parameters. Try: \n\t clone net \n\t clone fs\n");
	      free(input);
	      free(argvp);
	      continue;
	 }
	 if(strcmp(argvp[1], "net") == 0)
	      cloneInterface(CLONE_NEWNET);
    }
    else if(strcmp(argvp[argvSize-1],"&") == 0)
    {
      argvp[argvSize-1] = '\0';
      // no wait for bg process
      forkAndExecute(argvp, 0);
    }
    else
    {
      forkAndExecute(argvp, 1);
    }
    /* ---- End Body of Process Control ---- */
  
    free(input);
    free(argvp);
  }
}


int getInputWithoutDelimiter(char** input)
{
  size_t len = 0;
  ssize_t numchars = getline(input, &len, stdin);
  
  if(numchars == -1)
  {
    fprintf(stderr, "Failed to read input. \n");
    return -1;
  }

  if(*(*input + numchars -1)  == '\n')
  {
    *(*input + numchars -1) = '\0'; //null terminator
    --numchars;
  }

  return numchars;
}


int makeargv(const char *s, const char *delimiters, char ***argvp)
{
  int error;
  int i;
  int numTokens;
  const char *snew;
  char *t;

  if ((s == NULL) || (delimiters == NULL) || (argvp == NULL))
  {
    errno = EINVAL;
    return -1;
  }

  *argvp = NULL; //pointer to array of strings initialized to NULL

  /* Pointer arithmethic to make snew point to the real start of the 
   * string, as strspn returns the length of s which consists of 
   * delimiters. Hence snew is real start of string.
   */
  snew = s + strspn(s, delimiters); 

  // allocate memory for t
  if ((t = malloc(strlen(snew) + 1)) == NULL) // +1 for null term
    return -1;

  strcpy(t, snew); //strtok does in place tokenization
  numTokens = 0;
  if (strtok(t, delimiters) != NULL)
    // count number of tokens (to allocate buffer)
    for (numTokens = 1; strtok(NULL, delimiters) != NULL; numTokens++);

  // allocate mem for array of pointers to tokens
  if (( *argvp = malloc((numTokens + 1) * sizeof(char *))) == NULL)
  {
    error = errno;
    free(t);
    errno = error;
    return -1;
  }

  if (numTokens == 0)
    free(t);
  else 
  {
    strcpy(t, snew);
    **argvp = strtok(t, delimiters);
    for(i = 1; i < numTokens; i++)
      *( (*argvp) + i) = strtok(NULL, delimiters); 
  }
  
  *( (*argvp) + numTokens) = NULL; //put null pointer at end of argvp array

  return numTokens;
}

int forkAndExecute(char** argvp, int waitForProcess)
{
  pid_t pid;
  pid = fork();
  int status = 0;
  if (pid == 0) //child process
  {
    printf("CHILD process: %d \n", pid);
    if(execvp(argvp[0], argvp) < 0)
    {
	 fprintf(stderr,"Error, no command '%s' found or incorrect arguments.\n", argvp[0]);
	 exit(EXIT_FAILURE);
    } 
    _exit(0);
    //exit call is reached unless execvp returns with an error
    //execvp will replace the current running proc with the called proc
  }
  else if (pid > 0) //parent process
  {
    printf("PARENT process: %d \n", pid);
    if(waitForProcess)
    {
      while(waitpid(pid, &status, 0) < 0)
      {
	if(errno != EINTR)
	{
	  status = -1;
	  break;
	}
      }
    }
  }
  else //error
  {
    fprintf(stderr, "Error Forking Process. \n");
    status = -1;
  }
  return status;
}

int fn_testNetwork() {
     printf("\t --- NEW Network Namespace PID: %ld --- \n", (long)getpid());
     system("ip link");
     return 0;
}

int cloneInterface(int interface)
{
     char* stack = malloc(STACK_SIZE);
     char* stackTop = stack + STACK_SIZE;
     pid_t child_pid;

     if(interface == CLONE_NEWNET)
     {
	  printf("\t --- ORIGINAL Net Namespace: --- \n");
	  system("ip link");
	  // have to fork and exec to use this execl("/bin/sh", "sh", "-c", "ip link", (char*)0);
     }


     child_pid = clone(fn_testNetwork, stackTop, interface |CLONE_NEWPID | SIGCHLD, NULL);
     if(child_pid == -1)
	  printf("ERROR: Failed to clone interface. Are you running shell as sudo? \n");
     else
     {
	  printf("\n Cloned PID is: %ld\n", (long)child_pid);
	  waitpid(child_pid, NULL, 0);
     }

     free(stack);
     // cannot free stacktop, it will exit the shell.
     return child_pid;
}
