/* regex.h

   This file declares the functions [makeRegex] and [matchRegex].

   Author(s): Eric Van Wyk
 */
#ifndef REGEX_H
#define REGEX_H

#include <regex.h>

regex_t *makeRegex (const char* pattern) ;

int matchRegex (regex_t *, const char *) ;

#endif /* REGEX_H */
