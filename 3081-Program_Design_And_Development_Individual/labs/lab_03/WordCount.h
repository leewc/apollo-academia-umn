/* WordCount.h

   This file declares the functions [consumeWhiteSpaceAndComments] and
   [wordCount] that are use to count words, numeric constants, and
   "Boot" keywords, except for those not found in comments.

   Author(s): Eric Van Wyk, Dan Challou
*/
#ifndef WORDCOUNT_H
#define WORDCOUNT_H

#include <regex.h>

struct Results {
    int numWords;
    int numNumericConsts;
    int numBoots; } ;

int consumeWhiteSpaceAndComments (regex_t *whiteSpace, 
                                  regex_t *blockComment,
				  regex_t *lineComment,
                                  const char *text) ;

struct Results wordCount (const char *text) ;

#endif
