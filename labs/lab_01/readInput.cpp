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
    if (argc <= 1) {
        printf ("Usage: readInput <filename>\n") ;
        return 1 ;
    }

    printf ("Opening file \"%s\".\n", argv[1]);

    FILE *in_fp ;
    in_fp = fopen(argv[1],"r") ;
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

    while (ch != EOF) {
        buffer[index] = ch ;
        index ++ ; 
        ch = getc(in_fp);
    }
    buffer[index] = '\0' ;

    printf ("The contents of the file are:\n%s\n\n", buffer) ;

    return 0 ;
}
