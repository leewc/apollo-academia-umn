#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void shell_loop();
char* getInputWithoutDelimiter();

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
    char *input;

    printf("-$ ");
    input = getInputWithoutDelimiter();
    printf("%s \n", input);

    const char *ex = "exit";
    
    if(strcmp(input,ex) == 0)
    {
      run = 0;
    }
    free(input);
  }
}

char* getInputWithoutDelimiter()
{
  char* input = NULL;
  size_t len = 0;
  ssize_t numchars = getline(&input, &len, stdin);
  
  if(numchars == -1)
    fprintf(stderr, "Failed to read input. \n");
  if(input[numchars-1] == '\n')
  {
    input[numchars-1] = '\0'; //null terminator
    --numchars;
  }
  return input;
}
