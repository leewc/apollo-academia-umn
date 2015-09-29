#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/wait.h>
#include <unistd.h>

#define DELIMITERS " \n" //space, newlines are delimiters

void shell_loop();
int getInputWithoutDelimiter(char** input);
int makeargv(const char *s, const char *delimiters, char ***argvp);
int forkAndExecute(char** argvp, int waitForProcess); 

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
    printf("-$ ");

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

    int procStatus;
    if(strcmp(argvp[0],"exit") == 0 || strcmp(argvp[0],"quit") == 0)
    {
      run = 0;
      continue;
    }

    else if(strcmp(argvp[argvSize-1],"&") == 0)
    {
      procStatus = forkAndExecute(argvp, 0);
    }

    else
    {
      procStatus = forkAndExecute(argvp, 1);
    }

    /*
    int i;
    for (i = 0; i < argvSize; i++)
    printf("%s \n", argvp[i]);
    */
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

  int i=0;

  printf("Time to fork.. \n");
  pid = fork();
  int status;
  if (pid == 0) //child process
  {
    execvp(argvp[0], argvp);
  }
  else if (pid < 0) //error
  {
    fprintf(stderr, "Error Forking Process. \n");
    status = -1;
  }
  else //parent process
  {
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
  return status;
}
