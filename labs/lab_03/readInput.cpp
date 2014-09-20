/* readInput.cpp

   A simple function to read a file into a charachter buffer allocated
   by this function.

   Author(s): Eric Van Wyk
 */

#include <stdio.h>
#include <stdlib.h>

#include <sys/stat.h>
#include <sys/types.h>  

char *readInput (int argc, char **argv) {

    // Verify that a file name is provided and that the file exists.
    // Use some new C++ stream features.
    if (argc <= 1) {
        printf ("Usage: wordCount <filename>\n") ;
        return NULL ;
    }

    // ifstream in(argv[1]);
    FILE *in_fp ;
    in_fp = fopen(argv[1],"r") ;
    if ( in_fp==NULL ) {
        printf ("File \"%s\" not found.\n", argv[1]);
        return NULL ;
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

    return buffer ;
}
