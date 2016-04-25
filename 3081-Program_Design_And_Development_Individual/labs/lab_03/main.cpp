/* main.cpp

   This program counts words, numeric constants, and "Boot" keywords,
   except for those not found in comments that are contained in a
   file.  The file name is provided as a command line argument.

   Author(s): Eric Van Wyk, Dan Challou
*/

#include <stdio.h>

#include "readInput.h"
#include "WordCount.h"


int main(int argc, char **argv) {

    char *text = readInput(argc, argv) ;

    // If reading in input failed, exit with return code of 1.
    if (text==NULL) {
        return 1 ;
    }

    struct Results res = wordCount (text) ;

    printf ("%d\n", res.numWords) ;
    printf ("%d\n", res.numNumericConsts) ;
    printf ("%d\n", res.numBoots);
}
