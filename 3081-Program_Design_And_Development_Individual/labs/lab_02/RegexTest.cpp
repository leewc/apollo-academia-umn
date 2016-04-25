#include <stdio.h>
#include <stdlib.h>

#include <regex.h>
#include <sys/types.h>  

void match(const char *string, const char *pattern) ;

int main() {

    // Some strings for regular expressions.
    const char* word_re = "^[a-zA-Z]+" ;
    const char* whiteSpace_re = "^([\n\t\r ])+" ;
    const char* num_re = "^[0-9]*";
    const char* float_re = "[0-9]*.\[0-9]+";
    const char* l_parens_re = "\\{";   //first \ is to escape the \{, where the \ in \{ is to escape c-stirng, alternative -> [{]

    /* The match function lets you experiment with regular expressions.
       The first argument is the text to match against.
       The second is the string for the regular expression.
       To match only against the beginning of the text the regular
       expression must begin with the ^ character.
     */
    match ( "{\ left parens",
            l_parens_re) ;
}

/* An function to experiment with the regex.h library. */
void match(const char *text, const char *pattern) { 
    int status; 
    regex_t re; 
  
    int rc ;
    /* "Compile" the regular expression.  This sets up the regex to do
       the matching specified by the regular expression given as a
       character string.
     */
    rc = regcomp(&re, pattern, REG_EXTENDED) ;

    if (rc!= 0) {
        printf ("Error in compiling regular expression.\n");
        size_t length = regerror (rc, &re, NULL, 0) ;
        char *buffer = (char *) malloc( sizeof(char) * length ) ;
        (void) regerror (rc, &re, buffer, length) ;
        printf ("%s\n", buffer);
    }
  
    const int nsub=1 ;
    regmatch_t matches[nsub] ;

    /* execute the regular expression match against the text.  If it
       matches, the beginning and ending of the matched text are stored
       in the first element of the matches array.
     */
    status = regexec(&re, text, (size_t)nsub, matches, 0); 

    if (status==REG_NOMATCH) {
        printf ("No match\n") ;
    }
    else {
        printf ("A match\n") ;
        printf ("start: %d\n", (int) matches[0].rm_so ) ;
        printf ("end: %d\n", (int) matches[0].rm_eo ) ;
    }
    
    regfree(&re); 
}
  
