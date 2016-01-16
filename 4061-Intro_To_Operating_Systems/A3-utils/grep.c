#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>

void findInFile(char* keyword, char* filename);

int main(int argc, char** argv)
{
    if(argc != 3)
    {
        fprintf(stderr, "Usage: %s <string> <filename>\n", argv[0]);
        return 1;
    }
    
    
    struct stat f_stat;
    char* filename = argv[2];
    
    //check if given arg is a file
    if(stat(argv[2], &f_stat) == -1 ){
        fprintf(stderr, "%s does not exist or could not stat.\n", filename);
        return 1;
    }
        
    if(S_ISREG(f_stat.st_mode))
    {
        findInFile(argv[1], filename);
        return 0;
    }
    //not a regular file
    fprintf(stderr, "%s is not a regular file.\n", filename);
    return 1;
}

/*
    Checks if keyword exists in filename
    Ref: http://stackoverflow.com/questions/12784766/check-substring-exists-in-a-string-in-c
*/

void findInFile(char* keyword, char* filename)
{
    FILE* file = fopen(filename, "r"); //already checked it's a file in the previous function
    
    char *line = NULL;
    size_t len = 0;
    ssize_t read;
    
    int lineno = 0;     //keep track of each line (for printing)
    while ((read = getline(&line, &len, file)) != -1)
    {
        lineno++;
        if(strstr(line, keyword) != NULL) //found matching lines
            printf("%2d: %s", lineno, line);
    }
    
    free(line);
    fclose(file);
}

