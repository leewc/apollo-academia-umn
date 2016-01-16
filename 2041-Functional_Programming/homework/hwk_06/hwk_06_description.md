# Homework 6: Working with higher order functions, part 1

*CSci 2041: Advanced Programming Principles, Fall 2014*

**Due:** Friday, October 31 at 11:59pm

Note that part 2 will be due Friday, November 7 at 11:59pm.


## Introduction - The Paradelle



In this homework assignment you will write an OCaml program that
reads a text file and reports if it contains a poem that fits the
"fixed-form" style known as a *paradelle*.

Below is a sample paradelle called "Paradelle for Susan" by Billy
Collins from his book *Picnic, Lightning*.


> I remember the quick, nervous bird of your love. <br/>
> I remember the quick, nervous bird of your love. <br/>
> Always perched on the thinnest, highest branch. <br/> 
> Always perched on the thinnest, highest branch. <br/>
> Thinnest of love, remember the quick branch. <br/>
> Always nervous, I perched on your highest bird the.  
>
> It is time for me to cross the mountain.  <br/>
> It is time for me to cross the mountain.  <br/>
> And find another shore to darken with my pain.  <br/>
> And find another shore to darken with my pain.  <br/>
> Another pain for me to darken the mountain.  <br/>
> And find the time, cross my shore, to with it is to. 
>
> The weather warm, the handwriting familiar.  <br/>
> The weather warm, the handwriting familiar.  <br/>
> Your letter flies from my hand into the waters below. <br/>
> Your letter flies from my hand into the waters below. <br/>
> The familiar waters below my warm hand. <br/>
> Into handwriting your weather flies your letter the from the. 
>
> I always cross the highest letter, the thinnest bird. <br/>
> Below the waters of my warm familiar pain, <br/>
> Another hand to remember your handwriting. <br/>
> The weather perched for me on the shore. <br/>
> Quick, your nervous branch flies for love. <br/>
> Darken the mountain, time and find my into it with from to to is.


Following this poem, Collins provides the following description of this form:

>  The paradelle is one of the more demanding French fixed forms, first
appearing in the *langue d'oc* love poetry of the eleventh century.  It
is a poem of four six-line stanzas in which the first and second lines,
as well as the third and fourth lines of the first three stanzas, must
be identical.  The fifth and sixth lines, which traditionally resolve
these stanzas, must use *all* the words from the preceding
lines  ~~stanza~~ and *only* those words.  Similarly, the final stanza must
use *every* word from *all* the preceding stanzas and
*only* those words.

Collins is actually being satirical here and poking fun at overly
rigid fixed-form styles of poetry.  There is actually no form known as
the *paradelle*.  This did not stop people from going off and
trying to write their own however.  
In fact, the above poem is
slightly modified from his original so that it actually conforms to
the rules of a paradelle. 


To write an OCaml program to detect if a text file contains a paradelle
we add some more specific requirements to Collin's description above.
You should take these into consideration when completing this
assignment:

+  Blank lines are allowed, but we will assume that blank lines
  consist of only a single newline ``'\n'`` character. 

+  Punctuation and spacing (tabs and the space characters) should
  not affect the comparison of lines in a stanza.  For example, the
  following two lines would be considered as "identical" because the
  same words are used in the same order even though spacing and
  punctuation are different. 

  ``"And find  the time,cross my shore, to with it is to"``

  ``"And find the time , cross my shore, to with it is to ."``

  Thus, we will want to ignore punctuation symbols to some extent, 
  being careful to notice that they can separate words as in ``"that,barn"``.

  Specifically, the punctuation we will
  consider are the following : 
  
   ``.  !  ?  ,  ;  : -``

+ Also, we will need to split lines in the file (of Ocaml type
  ``string``) into a list of lines 
    and then split each line individual line  into a list of
    words.  In the list of words there
    should be no spaces, tabs, or punctuation symbols.  Then we can
    compare lists of words.

+ Capitalization does not matter.  The words ``"Thinnest"``
  and "``thinnest"`` are to be considered as the same.


+ In checking criteria for an individual stanza, each instance of
  a word is counted.  But in checking that the final stanza uses all
  the words of the first 3, duplicate words should be removed.


+ Your program must return a correct answer for any text file.
  For example, your program should report that an empty file or a file
  containing a single character or the source code for this assignment
  are not in the form of a paradelle.

Note that part 1 of this assignment, which is due on October 31, only
requires completion of some of these tasks, as described below.


## Getting started

In the same pattern as what we've done before, create a file
``hwk_06.ml`` and place it in a ``hwk_06`` directory in the
``homework`` directory in your indidual repository.

To get started you first want to copy a few functions from class
demonstrations into your ``hwk_06.ml`` file.  These can be found in
the lecture slides or in the code examples directory in the public
repositories.

First, copy the definitions of ``map``, ``filter``, ``foldl``, and
``foldr`` that we've used in lecture into ``hwk_06.ml``.

Then copy ``take`` and ``drop`` from your previous lab into this same
file.

These 6 functions are the only recursive functions that can be written
for this assignment.  All functions described below and all others that
you chose to write to implement the paradelle test must be either
non-recursive computations, or they must call one of the above higher
order functions, such as ``map``, ``filter``, ``foldl``, and
``foldr``, to carry out the computation.

In simpler terms, you may not use the ``rec`` keyword anywhere except
in the 6 functions ``map``, ``filter``, ``foldl``, and ``foldr``,
``take``, and ``drop``.

This restriction will help you start to think like a functional
programmer and give you a better understanding how higher order
functions can be used and written in OCaml and many other more
mainstream languages.

You are allowed to use ``String.to_list``

## Some useful functions.

Your first step is to define three functions that will be useful in
solving the paradelle check.

#### list membership

Define a function ``is_elem`` whose first argument is a value and second
argument is a list of values of the same type.  The function returns
``true`` if the value is in the list.

For example, ``is_elem 4 [1; 2; 3; 4; 5; 6; 7]`` should evaluate to
``true`` while ``is_elem 4 [1; 2; 3; 5; 6; 7]`` and ``is_elem 4 [ ]``
should both evaluate to ``false``.

Annotate your function with types or add a comment
indicating the type of the function.

#### a splitting function

Write a splitting function named ``split_by`` that takes three arguments

1. an equality checking function that takes two values
   and returns a value of type ``bool``,

2. a list of values that are to be separated,

3. and a list of separators values.


This function will split the second list into a list of lists.  If the
checking function indicates that an element of the first list
(the second argument) is an element of the second list (the third
argument) then that element indicates that the list should be split at
that point.  Note that this "spliting element" does not appear
in any list in the output list of lists.

For example, 
+ ``split_by (=) [1;2;3;4;5;6;7;8;9;10;11] [3;7]`` should evaluate to ``[
[1;2]; [4;5;6]; [8;9;10;11] ]`` and
+ ``split_by (=) ["A"; "B"; "C"; "D"] ["E"]`` should evaluate to ``[["A"; "B"; "C"; "D"]]``
 
Annotate your function with types or add a comment
indicating the type of the function.  

Also add a comment explaining the behavior of your function and its
type. Try to write this function so that the type is as general as
possible.

#### a length function

Write a function, named ``length`` that, as you would expect, takes a
list and returns its length as a value of type ``int``

Annotate your function with types or add a comment
indicating the type of the function.  


## Preparing text for the paradelle check.

The poems that we aim to check are stored as values of type ``string``
in text files.  But to check the paradelle criteria we need to break
the ``string`` into a list of lines of text, removing the blank lines,
and also splitting the lines of text into lists of words.

We need to write a function called
``convert_to_non_blank_lines_of_words`` that takes as input the poem
as an OCaml ``string`` and returns a list of lines, where each line is
a list of words, and each word is a list of characters.

Thus, ``convert_to_non_blank_lines_of_words`` can be seen as having
the type ``string -> char list list list``.

We can use the type system to name new types that make this type
easier to read.

First define the type ``word`` to be ``char list`` by
```
type word = char list
```
Then define a ``line`` type to be a ``word list``.

Then, we can specify that 
 ``convert_to_non_blank_lines_of_words`` has
the type ``string -> line list``.

In writing ``convert_to_non_blank_lines_of_words`` you may want to
consider a helper function that break up either a ``string`` or ``char
list`` into lines, separated by new line characters (``'\n'``) and
another that breaks up lines into lists of words.


At this point you are not required to directly address the problems relating to
capitalization of letters which we eventually need to address in
checking that the same words appear in various parts of the poem.  You
are also not required to deal with issues of punctuation, but you may
need to do something the be sure that words are correctly separated.
For example, we would want to see ``that,barn`` as two words.

## Reading files in OCaml

You may use the following function to read in a file when given the
name of that file.  If may fail and return ``None`` or succeed and
return the ``string`` in an ``option`` type.
```
let get_text (fn:string) : string option =
  try
      Some (In_channel.read_all fn)
  with 
  | _ -> None
```


## Assessments

+ ___ / 5: Functions are put into the files name
           ``homework/hwk_06/hwk_06.ml``.

+ ___ / 15: The file ``hwk_06.ml`` has no errors and no failing
            assertions.

+ The only recursive functions that have been written are 
  ``map``, ``filter``, ``foldl``, ``foldr``, ``take``, and ``drop``.
  All other functions that require a recursive computation use one of these to do so.

  In simpler terms, the ``rec`` keyword is not used anywhere except
  in the 6 functions ``map``, ``filter``, ``foldl``, and ``foldr``,
  ``take``, and ``drop``.


#### Sample executions.

The following assertions represent sample executions will form part of
the assessment of homework 6.  But they should not be seen as an
exhaustive set of test cases.  Assessments may included additional
tests.

You might add these to the bottom of your ``hwk_06.ml`` file and
COMMENT THEM ALL OUT.  Then uncomment them as you finish parts of the
problems.   They are wrapped in comments below.

FILES CHECKED IN WITH FAILING ASSERTIONS WILL NOT BE GRADED.

The text files mentioned in the assertions can be found in the
``homework/hwk_06`` directory of the public GitHub repository.
```
(*
assert (is_elem 4 [1;2;3;4;5;6])
assert (not (is_elem 7 [1;2;3;4;5;6;8;9;10] ) )
assert (is_elem "Hello" ["Why"; "not";  "say"; "Hello"])
assert (not (is_elem 3.5 [ ]) )


assert ( split_by (=) [1;2;3;4;5;6;7;8;9;10;11] [3;7] =
         [ [1;2]; [4;5;6]; [8;9;10;11] ] )
assert ( split_by (=) ["A"; "B"; "C"; "D"] [] =
         [["A"; "B"; "C"; "D"]] )


assert ( length [] = 0 )
assert ( length [1;2;3;4] = 4 )
assert ( length ["Hello"] = 1 )


assert ( let text = In_channel.read_all "paradelle_susan_1.txt"
         in length (convert_to_non_blank_lines_of_words text) = 24 )

assert ( let text = In_channel.read_all "paradelle_susan_2.txt"
         in length (convert_to_non_blank_lines_of_words text) = 24 )

assert ( let text = In_channel.read_all "paradelle_emma_1.txt"
         in length (convert_to_non_blank_lines_of_words text) = 24 )

assert ( let text = In_channel.read_all "not_a_paradelle_susan_1.txt"
         in length (convert_to_non_blank_lines_of_words text) = 24 )

assert ( let text = In_channel.read_all "not_a_paradelle_susan_2.txt"
         in length (convert_to_non_blank_lines_of_words text) = 24 )

assert ( let text = In_channel.read_all "not_a_paradelle_emma_1.txt"
         in length (convert_to_non_blank_lines_of_words text) = 24 )

assert ( let text = In_channel.read_all "not_a_paradelle_empty_file.txt"
         in length (convert_to_non_blank_lines_of_words text) = 0 )

assert ( let text = In_channel.read_all "not_a_paradelle_wrong_line_count.txt"
         in length (convert_to_non_blank_lines_of_words text) = 9 )

assert ( let text = In_channel.read_all "paradelle_susan_1.txt"
	 in  match convert_to_non_blank_lines_of_words text with
	     | line1::rest -> length line1 = 9
	     | _ -> false ) 
*)
```
 





