# Lab 8 - Improving the quality of OCaml pattern matching functions

*CSci 2041: Advanced Programming Principles, Fall 2014*

**Due** Friday, October 24 at 11:59pm


## Exam 1.

Exam 1 will be returned to you today.

The average score was 60, so was the median.

Keep your exam!  Any data-entry errors that are made in Moodle can
only be fixed if you have your original exam.

We will discuss the exam in lecture on Wednesday.



## Higher Order Functions

To warm up for homework 6 we will write a few functions that might be
useful in that problem.  (See the L10 slides for an informal
description.  The specifications will be published on GitHub on
Tuesday or Wednesday.)

The functions defined below should be in a file named ``lab_08.ml``
and place this file in a ``lab_08`` directory in your ``labs``
directory in your individual repository.

### take

Write a function ``take`` with the type ``int -> 'a list -> 'a list``
such that ``take n lst`` returns the first ``n`` elements of the
list.  If the list contains fewer than ``n`` elements then the entire
list is returned.

You should be able to write ``take`` without initially comparing ``n``
to the length of the list.  A simple ``match`` expression will be all
you need.

### drop

Write a function ``drop`` with type ``int -> 'a list -> 'a list``
such that ``drop n lst`` returns the remainder of the list ``lst``
after ``n`` elements have been removed.  If the length of the list is
less than ``n`` then the empty list is returned.

Again, you should be able to write ``drop`` without initially
comparing ``n`` to the length of the list.

### take_while

Write a function ``take_while`` with the type 
``('a -> bool) -> 'a list -> 'a list`` such that 
``take_while f lst`` returns the prefix of the list for which the
function ``f`` returns true.

### capitalize

Define the ``estring`` type as follows:
```
type estring = char list
```
and include the definitions for
``estring_to_string`` and ``string_to_estring`` from lecture in your
file.

Define ``capitalize`` to have type ``estring -> estring`` such that it
capitalizes all characters in the input list.

Do this by using ``map`` and not writing your own recursive function.


## Assessments

Your function


+ ___ / 5: Functions are put into the appropriate file:
           ``labs/lab_08/lab_08.ml``

+ ___ / 5: ``take 4 [1;2;3;4;5;6;7;8]`` should evaluate to
           ``[1;2;3;4]``

+ ___ / 5: ``take 6 [1.2; 2.3; 3.4; 4.5]`` should evaluate to
           ``[1.2; 2.3; 3.4; 4.5]``


+ ___ / 5: ``drop 4 [1;2;3;4;5;6;7;8]`` should evaluate to
           ``[5;6;7;8]``

+ ___ / 5: ``drop 6 [1.2; 2.3; 3.4; 4.5]`` should evaluate to
           ``[]``


+ ___ / 5: ``take_while (fun x -> x mod 2 = 0) [2;4;6;7]`` should
           evaluate to ``[2; 4; 6]``


+ ___ / 5: ``take_while (fun x -> x > 10) [2;4;6;7]`` should
           evaluate to ``[]``


+ ___/ 5: ``estring_to_string (capitalize (string_to_estring
            "Hello!"))`` should evaluate to ``"HELLO!"``
 

+ ___ / 5: ``capitalize []`` should evaluate to ``[]``
