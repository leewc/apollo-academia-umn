/* This program counts words and numbers, except for those not found
   in comments.

   Author(s): Eric Van Wyk
*/

#include <stdio.h>
#include <stdlib.h>

#include <regex.h>     //not sure if we need this?
#include <sys/stat.h>
#include <sys/types.h>  

#include "regex.h"    //definitely need this
#include "readInput.h"
#include "WordCount.h" 

int consumeWhiteSpaceAndComments (regex_t *whiteSpace, 
                                  regex_t *blockComment,
                                  regex_t *lineComment,
                                  const char *text) ;

struct Results wordCount(const char *text) {

  struct Results re;
 
    //char *text = readInput(argc, argv) ;  no longer needed as main.cpp handles this/

    // Create the compiled regular expressions.
    regex_t whiteSpace ;
    whiteSpace = *makeRegex ("^[\n\t\r ]+") ;

    regex_t blockComment ;
    blockComment = *makeRegex ("^/\\*([^\\*]|\\*+[^\\*/])*\\*+/");

    regex_t lineComment ;
    lineComment = *makeRegex ("^//[^\n]*\n");

    regex_t word ;
    word = *makeRegex ("^([a-zA-Z]+)") ;

    regex_t integerConst ;
    //makeRegex (&integerConst, "^[0-9]+") ;    
    // modified to include the count of floating point numbers
    // somehow using / instead of [] complains, ^ is needed to show front
    integerConst = *makeRegex ("^[0-9]*[.]*[0-9]+");
    
    //Add: Boot Regex is not ^[Boot]+ as that matches nonwords
    regex_t boot ;
    boot = *makeRegex ("^(Boot)") ;


    /* This enumerated type is used to keep track of what kind of
       construct was matched. 
     */
    enum MatchType { numMatch, wordMatch, bootMatch, noMatch } matchType ;

    int numMatchedChars = 0 ;

    // Consume leading white space and comments
    numMatchedChars = consumeWhiteSpaceAndComments (&whiteSpace, &blockComment, &lineComment, 
                                                    text) ;
    /* text is a character pointer that points to the current
       beginning of the array of characters in the input.  Adding an
       integer value to it advances the pointer that many elements in
       the array.  Thus, text is increased so that it points to the
       current location in the input. 
     */
    text = text + numMatchedChars ;

    int maxNumMatchedChars = 0 ;
    int numWords = 0, numNumericConsts = 0 ;
    int numBoots = 0;

    while ( text[0] != '\0' ) {
        maxNumMatchedChars = 0 ; matchType = noMatch ;

        /* maxNumMatchedChars is used to ensure that the regular
           expression that matched the longest string is the one that
           we use.  

           The regexs for word and integerConst cannot match the
           same text, but if we extend this program to search for
           specific keywords, then the keyword regex and the
           word-regex may, in some cases, match the same input text.

           If two regexs match the same number of characters
           then the tie has to be broken.  To break the tie, priority
           is given to the first one that was tried.  Thus the
           comparison
              (numMatchedChars > maxNumMatchedChars) 
           is strictly greater than.  Not greater than or  equal to.
        */

		// Add: BootMatch, which has to be above the normal wordMatch
		// this is more important than word as it has to take precedence over the word regex
		numMatchedChars = matchRegex (&boot, text) ;
        if (numMatchedChars > maxNumMatchedChars) {
            maxNumMatchedChars = numMatchedChars ;
            matchType = bootMatch ;
		}
		

        // Try to match a word
        numMatchedChars = matchRegex (&word, text) ;
        if (numMatchedChars > maxNumMatchedChars) {
            maxNumMatchedChars = numMatchedChars ;
            matchType = wordMatch ;
        }

        // Try to match an integer constant
        numMatchedChars = matchRegex (&integerConst, text) ;
        if (numMatchedChars > maxNumMatchedChars) {
            maxNumMatchedChars = numMatchedChars ;
            matchType = numMatch ;
        }
		
        switch (matchType) 
        {
	case bootMatch: ++numBoots; break; 
        case wordMatch: ++numWords; break;
        case numMatch: ++numNumericConsts; break;
        case noMatch: ;
        }

        if (matchType == noMatch) {
            // If we didn't match anything, then just skip the first character.
            text = text + 1 ;
        }
        else {
            // Consume the characters that were matched.
            text = text + maxNumMatchedChars ;
        }

        // Consume white space and comments before trying again for
        // another word or integer.
        numMatchedChars = consumeWhiteSpaceAndComments (&whiteSpace, &blockComment, &lineComment, 
                                                        text) ;
        text = text + numMatchedChars ;

    }

    /* In this application the only information we collect is the
       number of words and number of integer constants.  In a scanner
       we would need to accumulate the list of tokens. */
    re.numWords = numWords ;
    re.numNumericConsts = numNumericConsts ;
    re.numBoots = numBoots ;

    return re;
    /* You will add another printf statement to print the number of
       "John" keywords.  All of these numbers should be on separate
       lines.  In assessing your work we will require that your output
       exactly match ours: no extra spaces and each number on a
       separate line. */
}


int consumeWhiteSpaceAndComments (regex_t *whiteSpace, 
                                  regex_t *blockComment, 
				  regex_t *lineComment,
                                  const char *text) {
    int numMatchedChars = 0 ;
    int totalNumMatchedChars = 0 ;
    int stillConsumingWhiteSpace ;

    do {
        stillConsumingWhiteSpace = 0 ;  // exit loop if not reset by a match

        // Try to match white space
        numMatchedChars = matchRegex (whiteSpace, text) ;
        totalNumMatchedChars += numMatchedChars ;
        if (numMatchedChars > 0) {
            text = text + numMatchedChars ;
            stillConsumingWhiteSpace = 1 ;
        }

        // Try to match block comments
        numMatchedChars = matchRegex (blockComment, text) ;
        totalNumMatchedChars += numMatchedChars ;
        if (numMatchedChars > 0) {
            text = text + numMatchedChars ;
            stillConsumingWhiteSpace = 1 ;
        }

        // Try to match single-line comments
        numMatchedChars = matchRegex (lineComment, text) ;
        totalNumMatchedChars += numMatchedChars ;
        if (numMatchedChars > 0) {
            text = text + numMatchedChars ;
            stillConsumingWhiteSpace = 1 ;
        }
    }
    while ( stillConsumingWhiteSpace ) ;    

    return totalNumMatchedChars ;
}


