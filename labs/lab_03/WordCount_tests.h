#include <cxxtest/TestSuite.h>

#include "WordCount.h"
#include "regex.h"

using namespace std ;

class WordCountTestSuite : public CxxTest::TestSuite 
{
public:

    // Some simple sample tests to illustrate the assertion macros.
    void test_addition_sample () {
        TS_ASSERT ( 1 + 2 == 3 ) ;
    }
    void test_addition_equality_sample () {
        TS_ASSERT_EQUALS ( 1 + 2, 3 ) ;
    }

    // Tests for makeRegex
    // --------------------------------------------------
    /* These tests are ones that we might write to verify our
       understanding of how the functions work.  Even if we didn't
       write them and are not try to test them for bugs, writing tests
       can help understand how they do work.  */

    void test_makeRegex_some_digits () {
        regex_t *re = makeRegex ("[0-9]+") ;
        TS_ASSERT (re) ;
    }
    void test_makeRegex_xs_followed_by_ys () {
        regex_t *re = makeRegex ("x+y+") ;
        TS_ASSERT (re) ;
    }
    void test_makeRegex_fail_unbalanced_brackets (void) {
        regex_t *re = makeRegex ("[0-9]+[") ;
        TS_ASSERT (re == NULL) ;
    }
    void test_makeRegex_fail_illformed_backslash (void) {
        regex_t *re = makeRegex ("[0-9]+\\") ;
        TS_ASSERT (re == NULL) ;
    }

    /* T1. (1 test) Add a test that intentionally fails to create a
       regex because the regex string is not well formed. This test
       should be similar to [test_makeRegex_fail_illformed_brackets]. 
     */

    // Tests for matchRegex
    // --------------------------------------------------
    /* These tests are like those above, they help us understand how
       to use the functions.  */

    void test_matchRegex_abc_anywhere () {
        regex_t *re = makeRegex ("abc") ;
        TS_ASSERT (re) ;
        int numMatchedChars = matchRegex (re, " abc ") ;
        TS_ASSERT_EQUALS (numMatchedChars, 4) ;
        // numMatched is number chars consumed in finding the match.
    }

    void test_matchRegex_abc_at_beginning () {
        regex_t *re = makeRegex ("^abc") ;
        TS_ASSERT (re) ;
        int numMatchedChars = matchRegex (re, "abc ") ;
        TS_ASSERT_EQUALS (numMatchedChars, 3) ;
        // numMatched is number chars consumed in finding the match.
    }

    void test_matchRegex_fail_abc_anywhere () {
        regex_t *re = makeRegex ("abc") ;
        TS_ASSERT (re) ;
        int numMatchedChars = matchRegex (re, " a bc ") ;
        TS_ASSERT_EQUALS (numMatchedChars, 0) ;
    }

    void test_matchRegex_fail_abc_at_beginning () {
        regex_t *re = makeRegex ("^abc") ;
        TS_ASSERT (re) ;
        int numMatchedChars = matchRegex (re, " abc ") ;
        TS_ASSERT_EQUALS (numMatchedChars, 0) ;
    }

    /* T2. (1 test) Add a test that correctly creates a regex that
       then fails to match because the pattern is not present in the
       regular expression.  This test should be similar to the test
       [test_matchRegex_fail_abc_at_beginning]. 
     */

    // Tests of makeRegex and matchRegex for WordCount
    // --------------------------------------------------
    /* Here we want to write tests that ensure the we have written the
       correct regular expression string for the different types of
       patterns that we need to match for the WordCount program. 

       These create the regex_t and then try to match it.  These only
       need match at the beginning of the text. */

    void test_make_matchRegex_word () {
        regex_t *re = makeRegex ("^([a-zA-Z]+)") ;
        TS_ASSERT (re) ;
        int numMatchedChars = matchRegex (re, "something ") ;
        TS_ASSERT_EQUALS (numMatchedChars, 9) ;
    }

    /* T3. (5 tests) Write tests similar to [test_make_matchRegex_word]
       for the other patterns we care about for WordCount.  Thus we
       need a test for whitespace, block-comments, integer constants,
       floating point constants, and Boot keywords.

       Write your tests below.
    */


    // Tests for consumeWhiteSpaceAndComments.
    // --------------------------------------------------
    /* The tests above should confirm that we can make and match
       individual regular expressions for white space and block
       comments.  We now need to test that
       [consumeWhiteSpaceAndComments] properly does this and can match
       a sequence of these patterns. */ 

    /* T4. (3 tests) Write three tests that show
       [consumeWhiteSpaceAndComments] working on a sequence of
       white-space and block comments.  One of these should test that
       this function does the right thing when that sequence include 0
       such items.

       Write your tests below.
    */


    // Tests for wordCount.
    // --------------------------------------------------
    /* Having shown the the functions used by wordCount pass our
       tests, we have some confidence in them.  We can not test
       wordCount directly. */

    /* T5. (4 tests) Tests that show each element (word, integer
       constant, float constant, and Boot keyword) can be recognized
       when it is the only thing in the text besides perhaps some
       white space.

       We've provide an example of this for words.  Add four more
       tests, one for each other element.
     */

    void test_wordCount_single_word () {
        TS_ASSERT_EQUALS (wordCount (" someting ").numWords, 1 )  ;        
    }


    /* T6. (2 tests) We can now write some tests that include several
       elements. These test should check the contents of the returned
       structure to see that the right number of words, numbers and
       boot keywords have been matched.

       You should now write at least two tests of this type.  You will
       want to consider the case when there are zero words (or numbers
       or Boot keywords) in the text.

       Write your tests below.
     */


} ;





