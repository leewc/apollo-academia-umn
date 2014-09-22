/* Generated file, do not edit */

#ifndef CXXTEST_RUNNING
#define CXXTEST_RUNNING
#endif

#define _CXXTEST_HAVE_STD
#define _CXXTEST_HAVE_EH
#define _CXXTEST_ABORT_TEST_ON_FAIL
#include <cxxtest/TestListener.h>
#include <cxxtest/TestTracker.h>
#include <cxxtest/TestRunner.h>
#include <cxxtest/RealDescriptions.h>
#include <cxxtest/TestMain.h>
#include <cxxtest/ErrorPrinter.h>

int main( int argc, char *argv[] ) {
 int status;
    CxxTest::ErrorPrinter tmp;
    CxxTest::RealWorldDescription::_worldName = "cxxtest";
    status = CxxTest::Main< CxxTest::ErrorPrinter >( tmp, argc, argv );
    return status;
}
bool suite_WordCountTestSuite_init = false;
#include "/home/wclee/3081repo/repo-leex7095/labs/lab_03/WordCount_tests.h"

static WordCountTestSuite suite_WordCountTestSuite;

static CxxTest::List Tests_WordCountTestSuite = { 0, 0 };
CxxTest::StaticSuiteDescription suiteDescription_WordCountTestSuite( "WordCount_tests.h", 8, "WordCountTestSuite", suite_WordCountTestSuite, Tests_WordCountTestSuite );

static class TestDescription_suite_WordCountTestSuite_test_addition_sample : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_addition_sample() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 13, "test_addition_sample" ) {}
 void runTest() { suite_WordCountTestSuite.test_addition_sample(); }
} testDescription_suite_WordCountTestSuite_test_addition_sample;

static class TestDescription_suite_WordCountTestSuite_test_addition_equality_sample : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_addition_equality_sample() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 16, "test_addition_equality_sample" ) {}
 void runTest() { suite_WordCountTestSuite.test_addition_equality_sample(); }
} testDescription_suite_WordCountTestSuite_test_addition_equality_sample;

static class TestDescription_suite_WordCountTestSuite_test_makeRegex_some_digits : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_makeRegex_some_digits() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 27, "test_makeRegex_some_digits" ) {}
 void runTest() { suite_WordCountTestSuite.test_makeRegex_some_digits(); }
} testDescription_suite_WordCountTestSuite_test_makeRegex_some_digits;

static class TestDescription_suite_WordCountTestSuite_test_makeRegex_xs_followed_by_ys : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_makeRegex_xs_followed_by_ys() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 31, "test_makeRegex_xs_followed_by_ys" ) {}
 void runTest() { suite_WordCountTestSuite.test_makeRegex_xs_followed_by_ys(); }
} testDescription_suite_WordCountTestSuite_test_makeRegex_xs_followed_by_ys;

static class TestDescription_suite_WordCountTestSuite_test_makeRegex_fail_unbalanced_brackets : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_makeRegex_fail_unbalanced_brackets() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 35, "test_makeRegex_fail_unbalanced_brackets" ) {}
 void runTest() { suite_WordCountTestSuite.test_makeRegex_fail_unbalanced_brackets(); }
} testDescription_suite_WordCountTestSuite_test_makeRegex_fail_unbalanced_brackets;

static class TestDescription_suite_WordCountTestSuite_test_makeRegex_fail_illformed_backslash : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_makeRegex_fail_illformed_backslash() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 39, "test_makeRegex_fail_illformed_backslash" ) {}
 void runTest() { suite_WordCountTestSuite.test_makeRegex_fail_illformed_backslash(); }
} testDescription_suite_WordCountTestSuite_test_makeRegex_fail_illformed_backslash;

static class TestDescription_suite_WordCountTestSuite_test_makeRegex_fail_illformed_backets : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_makeRegex_fail_illformed_backets() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 55, "test_makeRegex_fail_illformed_backets" ) {}
 void runTest() { suite_WordCountTestSuite.test_makeRegex_fail_illformed_backets(); }
} testDescription_suite_WordCountTestSuite_test_makeRegex_fail_illformed_backets;

static class TestDescription_suite_WordCountTestSuite_test_matchRegex_abc_anywhere : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_matchRegex_abc_anywhere() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 62, "test_matchRegex_abc_anywhere" ) {}
 void runTest() { suite_WordCountTestSuite.test_matchRegex_abc_anywhere(); }
} testDescription_suite_WordCountTestSuite_test_matchRegex_abc_anywhere;

static class TestDescription_suite_WordCountTestSuite_test_matchRegex_abc_at_beginning : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_matchRegex_abc_at_beginning() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 70, "test_matchRegex_abc_at_beginning" ) {}
 void runTest() { suite_WordCountTestSuite.test_matchRegex_abc_at_beginning(); }
} testDescription_suite_WordCountTestSuite_test_matchRegex_abc_at_beginning;

static class TestDescription_suite_WordCountTestSuite_test_matchRegex_fail_abc_anywhere : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_matchRegex_fail_abc_anywhere() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 78, "test_matchRegex_fail_abc_anywhere" ) {}
 void runTest() { suite_WordCountTestSuite.test_matchRegex_fail_abc_anywhere(); }
} testDescription_suite_WordCountTestSuite_test_matchRegex_fail_abc_anywhere;

static class TestDescription_suite_WordCountTestSuite_test_matchRegex_fail_abc_at_beginning : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_matchRegex_fail_abc_at_beginning() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 85, "test_matchRegex_fail_abc_at_beginning" ) {}
 void runTest() { suite_WordCountTestSuite.test_matchRegex_fail_abc_at_beginning(); }
} testDescription_suite_WordCountTestSuite_test_matchRegex_fail_abc_at_beginning;

static class TestDescription_suite_WordCountTestSuite_test_match_makeRegex_pattern_not_present : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_match_makeRegex_pattern_not_present() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 109, "test_match_makeRegex_pattern_not_present" ) {}
 void runTest() { suite_WordCountTestSuite.test_match_makeRegex_pattern_not_present(); }
} testDescription_suite_WordCountTestSuite_test_match_makeRegex_pattern_not_present;

static class TestDescription_suite_WordCountTestSuite_test_make_matchRegex_word : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_make_matchRegex_word() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 117, "test_make_matchRegex_word" ) {}
 void runTest() { suite_WordCountTestSuite.test_make_matchRegex_word(); }
} testDescription_suite_WordCountTestSuite_test_make_matchRegex_word;

static class TestDescription_suite_WordCountTestSuite_test_make_matchRegex_integerConsts : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_make_matchRegex_integerConsts() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 134, "test_make_matchRegex_integerConsts" ) {}
 void runTest() { suite_WordCountTestSuite.test_make_matchRegex_integerConsts(); }
} testDescription_suite_WordCountTestSuite_test_make_matchRegex_integerConsts;

static class TestDescription_suite_WordCountTestSuite_test_make_matchRegex_whiteSpace : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_make_matchRegex_whiteSpace() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 142, "test_make_matchRegex_whiteSpace" ) {}
 void runTest() { suite_WordCountTestSuite.test_make_matchRegex_whiteSpace(); }
} testDescription_suite_WordCountTestSuite_test_make_matchRegex_whiteSpace;

static class TestDescription_suite_WordCountTestSuite_test_make_matchRegex_blockComments : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_make_matchRegex_blockComments() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 149, "test_make_matchRegex_blockComments" ) {}
 void runTest() { suite_WordCountTestSuite.test_make_matchRegex_blockComments(); }
} testDescription_suite_WordCountTestSuite_test_make_matchRegex_blockComments;

static class TestDescription_suite_WordCountTestSuite_test_make_matchRegex_floatingPointConsts : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_make_matchRegex_floatingPointConsts() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 156, "test_make_matchRegex_floatingPointConsts" ) {}
 void runTest() { suite_WordCountTestSuite.test_make_matchRegex_floatingPointConsts(); }
} testDescription_suite_WordCountTestSuite_test_make_matchRegex_floatingPointConsts;

static class TestDescription_suite_WordCountTestSuite_test_make_matchRegex_Boot : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_make_matchRegex_Boot() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 163, "test_make_matchRegex_Boot" ) {}
 void runTest() { suite_WordCountTestSuite.test_make_matchRegex_Boot(); }
} testDescription_suite_WordCountTestSuite_test_make_matchRegex_Boot;

static class TestDescription_suite_WordCountTestSuite_test_consumeWhiteSpaceAndComments_1 : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_consumeWhiteSpaceAndComments_1() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 188, "test_consumeWhiteSpaceAndComments_1" ) {}
 void runTest() { suite_WordCountTestSuite.test_consumeWhiteSpaceAndComments_1(); }
} testDescription_suite_WordCountTestSuite_test_consumeWhiteSpaceAndComments_1;

static class TestDescription_suite_WordCountTestSuite_test_consumeWhiteSpaceAndComments_empty : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_consumeWhiteSpaceAndComments_empty() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 198, "test_consumeWhiteSpaceAndComments_empty" ) {}
 void runTest() { suite_WordCountTestSuite.test_consumeWhiteSpaceAndComments_empty(); }
} testDescription_suite_WordCountTestSuite_test_consumeWhiteSpaceAndComments_empty;

static class TestDescription_suite_WordCountTestSuite_test_consumeWhiteSpaceAndComments_mix : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_consumeWhiteSpaceAndComments_mix() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 207, "test_consumeWhiteSpaceAndComments_mix" ) {}
 void runTest() { suite_WordCountTestSuite.test_consumeWhiteSpaceAndComments_mix(); }
} testDescription_suite_WordCountTestSuite_test_consumeWhiteSpaceAndComments_mix;

static class TestDescription_suite_WordCountTestSuite_test_wordCount_single_word : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_wordCount_single_word() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 233, "test_wordCount_single_word" ) {}
 void runTest() { suite_WordCountTestSuite.test_wordCount_single_word(); }
} testDescription_suite_WordCountTestSuite_test_wordCount_single_word;

static class TestDescription_suite_WordCountTestSuite_test_wordCount_single_word_Boot : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_wordCount_single_word_Boot() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 237, "test_wordCount_single_word_Boot" ) {}
 void runTest() { suite_WordCountTestSuite.test_wordCount_single_word_Boot(); }
} testDescription_suite_WordCountTestSuite_test_wordCount_single_word_Boot;

static class TestDescription_suite_WordCountTestSuite_test_wordCount_single_word_int : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_wordCount_single_word_int() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 241, "test_wordCount_single_word_int" ) {}
 void runTest() { suite_WordCountTestSuite.test_wordCount_single_word_int(); }
} testDescription_suite_WordCountTestSuite_test_wordCount_single_word_int;

static class TestDescription_suite_WordCountTestSuite_test_wordCount_single_word_float : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_wordCount_single_word_float() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 246, "test_wordCount_single_word_float" ) {}
 void runTest() { suite_WordCountTestSuite.test_wordCount_single_word_float(); }
} testDescription_suite_WordCountTestSuite_test_wordCount_single_word_float;

static class TestDescription_suite_WordCountTestSuite_test_wordCount_single_notWord : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_wordCount_single_notWord() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 250, "test_wordCount_single_notWord" ) {}
 void runTest() { suite_WordCountTestSuite.test_wordCount_single_notWord(); }
} testDescription_suite_WordCountTestSuite_test_wordCount_single_notWord;

static class TestDescription_suite_WordCountTestSuite_test_WordCount_mix_empty : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_WordCount_mix_empty() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 265, "test_WordCount_mix_empty" ) {}
 void runTest() { suite_WordCountTestSuite.test_WordCount_mix_empty(); }
} testDescription_suite_WordCountTestSuite_test_WordCount_mix_empty;

static class TestDescription_suite_WordCountTestSuite_test_WordCount_mix : public CxxTest::RealTestDescription {
public:
 TestDescription_suite_WordCountTestSuite_test_WordCount_mix() : CxxTest::RealTestDescription( Tests_WordCountTestSuite, suiteDescription_WordCountTestSuite, 273, "test_WordCount_mix" ) {}
 void runTest() { suite_WordCountTestSuite.test_WordCount_mix(); }
} testDescription_suite_WordCountTestSuite_test_WordCount_mix;

#include <cxxtest/Root.cpp>
const char* CxxTest::RealWorldDescription::_worldName = "cxxtest";
