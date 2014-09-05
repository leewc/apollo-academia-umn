/* A sample file to read the contents of a file into a 
   character buffer.

Author: Eric Van Wyk

Modifications for Lab 01 by:   <add your name here>
*/

#include <stdio.h>
#include <stdlib.h>
#include <sys/stat.h>

int main(int argc, char** argv) {

    printf ("Reading a file into a character buffer.\n");

    // Verify that a file name is provided and that the file exists.
    // Use some new C++ stream features.
	// This part of the code tells the user how to use the c++ program.
    if (argc <= 1) {
        printf ("Usage: readInput <filename>\n") ;
        return 1 ;
    }
    // Prints the name of the file to be opened.
    printf ("Opening file \"%s\".\n", argv[1]);

    // pointer to receive the file
    FILE *in_fp ;
    in_fp = fopen(argv[1],"r") ;

    // outputs to the terminal if no file is found or empty file and then return error number 2.
    if ( in_fp==NULL ) {
        printf ("File \"%s\" not found.\n", argv[1]);
        return 2 ;
    }
    // Determine the size of the file, used to allocate the char buffer.
    struct stat filestatus;
    stat( argv[1], &filestatus );

    int filesize = filestatus.st_size + 1; // +1 for terminating null char

    // Allocate space for the character buffer.
    char *buffer = (char *) malloc( sizeof(char) * filesize ) ;


    int index = 0 ;
    char ch = getc(in_fp) ;

    // a while loop that continues as long as the End-Of-File is not reached.
    // the loop assigns ch to every array index in the buffer, increments the index and repeats the process
    while (ch != EOF) {
        buffer[index] = ch ;
        index ++ ; 
        ch = getc(in_fp);
    }
    // assigns the last array slot with \0, to indicate the end of the buffer.
    buffer[index] = '\0' ;

    // Prints out every character in the file, including the \0. 
    printf ("The contents of the file are:\n%s\n\n", buffer) ;

    return 0 ;
}
