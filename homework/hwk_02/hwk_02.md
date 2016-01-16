# Homework 2: OCaml introduction

*CSci 2041: Advanced Programming Principles, Fall 2014*

**Due:** Monday, September 15 at 5:00pm

## Updates / Corrections
These corrections are fixed in the text below.
+ Your file should be named ``hwk_02.ml`` not ``hwk_02.md``
+ ``square_approx`` takes the accuracy as its first argument and the value for which
 to take the square root as its second.
+ ``matrix_scalar_addition`` should be named ``matrix_scalar_add``


## Introduction

Below, you are asked to write a number of OCaml functions.  Some are simple, such as a 
function to determine if an integer input is even or not.  Others are more interesting
and ask you to compute the square root of a floating point number to a specified degree
of accuracy.

Designing and implementing these functions will give you the opportunity to test
your knowledge of OCaml and how to write recursive functions in it.  Successfully
completing these will set you up for the more advanced (and more interesting) 
topics covered in this course.

Recall that while labs are meant to be done collaboratively, this work is meant to
be done on your own.

## Designing and implementing functions in OCaml

All functions should be placed in a file named ``hwk_02.ml`` which resides in a directory
named ``hwk_02``.  This directory should be in a directory named ``homework`` in your GitHub
repository.  That is, you need the path ~~homework/hwk_02/hwk_02.md~~ ``homework/hwk_02/hwk_02.ml`` 
to exist in your
repository.

In implementing these functions, do not use any functions from the ``List`` module.  If you
need some helper functions over lists, write them yourself.

Also, you should only use the pure, non-imperative features of OCaml.  No while-loops or references.
But since we've not discussed these they are easy to avoid.

### even or odd

Write an OCaml function named ``even`` with the type ``int -> bool`` that returns ``true``
if its input is even, ``false`` otherwise.

Recall that we used the OCaml infix operator ``mod`` in class.  You may find it useful here.



### Another GCD, Euclid's algorithmm

In class we wrote a greatest common divisor function that computed the GCD
of two positive integers by counting down by 1 from an initial value that was
greater than or equal to the GCD until we reached a common divisor.

You are now asked to write another GCD function that is both simpler to write
and faster.

This one is based on the following observations:
+ gcd(a,b) = a, if a = b
+ gcd(a,b) = gcd(a, b-a), if a<b
+ gcd(a,b) = gcd(a-b,b) if a>b

This function should be named ``euclid`` and have the type ``int -> int -> int``.



### Adding and multiplying fractions

We can use OCaml's tuples to represent fractions as a pair of integers.  For example, the value
``(1,2)`` of type ``int * int`` represents the value one-half; ``(5,8)`` represents the value five-eighths.

Consider the following function for multiplying two fractions
```
let frac_mul (n1,d1) (n2,d2) = (n1 *n2, d1 * d2)
```
It has type ``int * int -> int * int -> int * int``.

The expression ``frac_mul (1,2) (1,3)`` evaluates to ``(1,6)``.

Now write a function named ``frac_add`` that adds two fractions.  It should have the same
type as our addition function: ``(int * int) -> (int * int) -> (int * int)``.

You may assume that the denominator of any fraction is never 0.

Some example evaluations:
+ ``frac_add (1,2) (1,3)`` evaluates to ``(5,6)``
+ ``frac_add (1,4) (1,4)`` evaluates to ``(8,16)``
We see here that your addition function need not simplify fractions, that is the 
job of the next function.

### Simplifiying fractions

Write another fraction function that simplifies fractions.  It should be called
``frac_simplify`` with type ``(int * int) -> (int * int)``.

Consider the following sample evaluations:
+ ``frac_simplify (8,16)`` evaluates to ``(1,2)``
+ ``frac_simplify (4,9)`` evaluates to ``(4,9)``
+ ``frac_simplify (3,9)`` evaluates to ``(1,3)``

As before, you may assume that the denominator is never 0.

You may want to use your ``euclid`` function in writing ``frac_simplify``.


### Square root approximation

Consider the following algorithms written in psuedo-code similar to C.  
Assume that the "input" value ``n`` is greater than 1.0 and all variables
hold real numbers.
```
lower = 1.0;
upper = n;
accuracy = 0.001;
while ( (upper-lower) > accuracy ) {
  guess = (lower + upper) / 2.0;
  if ( (guess*guess) > n)
     upper = guess;
  else
     lower = guess;
}
```
After this algorithm terminates we know that 
*upper >= sqrt(n) >= lower* and *upper - lower <= accuracy*.
That is, lower and upper proivde a bound on the
actual square root of n and that this bound is within the specified accuracy.

You are asked to write a function named ``square_approx`` with type ``float -> float -> (float * float)``
that implements the above imperative algorithm, returning a pair of values corresponding to 
``lower`` and ``upper`` in the imperative psuedo-code.

The ~~first~~ second argument corresponds to ``n``, the value of which we want to take the square root, 
and the ~~second~~ first corresponds to ``accuracy``.

Of course, this should be a recursive function that does not use any of OCaml's imperative
features such as while-loops and references.

Consider the gcd function that we wrote in class since it has some characteristics that 
are similar to those needed for this function - namely the need to carry additional changing
values along the chain of recursive function calls as additional parameters.

### Maximum in a list

Write a function ``max_list`` that takes a list of integers as input and returns the maximum.
This function should have the type ``int list -> int``.

In your solution, write a comment that specifies any restrictions on the lists that can
be passed as input to your function.

### Dropping list elements

Write another list processing function called ``drop`` with type ``int -> int list -> int list``
that drops a specified number of elements from the input list.

For example, consider these evaluations:
+ ``drop 3 [1; 2; 3; 4; 5]`` evaluates to ``[4; 5]``
+ ``drop 5 ["A"; "B"; "C"]`` evaluates to ``[ ]``
+ ``drop 0 [1]`` evaluates to ``[1]``

You may assume that only non-negative numbers will be passed as the first argument to ``drop``.


### List reverse

Write a function named ~~reverse~~ ``rev`` that takes a list and returns the reverse of that list.

Recall that ``@`` is the list append operator, you may find this useful.


### Representing matrices as lists of lists

We could consider representing matrices as lists of lists of numbers.  For example
the list ``[ [1; 2; 3] ; [4; 5; 6] ]`` might represent a matrix with two rows (each row corresponding
to one of the "inner" lists) and three columns.

Here the type is ``int list list`` - a list of integer lists.

Of course, the type allows for values that do not correspond to matrices. For example,
``[ [1; 2; 3] ; [4; 5] ]`` would not represent a matrix since the first "row" has 3 elements and
the second has only 2.

Write a function ``is_matrix`` that takes in values such as the list of lists given above
and returns a boolean value of ``true`` if the list of lists represents a proper matrix and 
``false`` otherwise.

This function checks that all the "inner" lists have the same length.  
Since you are not to use any library functions you need to write your own function to determine 
the length of a list.


### A simple matrix operation: matrix scalar addition

Write a function, ~~matrix_scalar_addition~~ ``matrix_scalar_add`` with type ``int list list -> int -> int list list``
that implements matrix scalar addition.  This is simply the operation of adding the integer value
to each element of the matrix.

For example,
+ ``matrix_scalar_add [ [1; 2 ;3]; [4; 5; 6] ]  5`` evaluates to ``[ [6; 7; 8]; [9; 10; 11] ]``

You may assume that only matrices for which ``is_matrix`` evaluates to ``true`` are passed to this function.


## Bonus round

For a small number of extra credit points implement a matrix transpose function 
named ``matrix_transpose`` that has type ``'a list list -> 'a list list``.  It should transpose a matrix such as 
``[ [1; 2; 3]; 4; 5; 6] ]`` into ``[ [1; 4]; [2; 5]; [3; 6] ]``.

If you're feeling ambitious, try a matrix multiply function as well.  To simplify this,
we'll assume that matrices
hold integers and thus your ``matrix_multiply`` function should have type
``int list list -> int list list -> int list list``.



## Assessment
+ ___ / 5: Functions are put into the appropriate file: ``homework/hwk_02/hwk_02.md``.  
   The ``homework`` directory exists next to your existing ``labs`` directory.

+ ___ / 1: ``even 4`` evaluates to ``true``

+ ___ / 1: ``even 5`` evaluates to ``false``

+ ___ / 5: ``euclid 6 9`` evaluates to ``3``

+ ___ / 5: ``euclid 5 9`` evaluates to ``1``

+ ___ / 2: ``frac_add (1,2) (1,3)`` evaluates to ``(5,6)``

+ ___ / 3: ``frac_add (1,4) (1,4)`` evaluates to ``(8,16)``

+ ___ / 2: ``frac_simplify (4,9)`` evaluates to ``(4,9)``

+ ___ / 3: ``frac_simplify (3,9)`` evaluates to ``(1,3)``

+ ___ / 7: ``approx_squareroot 0.001 9.0`` evaluates to ``(3.,3.0009765625)``

+ ___ / 8: ``approx_squareroot 0.1 81.0`` evaluates to ``(8.96875,9.046875)``


+ ___ / 5: ``max_list [1; 2; 5; 3; 2]`` evaluates to ``5``
+ ___ / 5: ``max_list [-1; -2; -5; -3; -2]`` evaluates to ``-1``

+ ___ / 4: ``drop 3 [1; 2; 3; 4; 5]`` evaluates to ``[4; 5]``
+ ___ / 3: ``drop 5 ["A"; "B"; "C"]`` evaluates to ``[ ]``
+ ___ / 3: ``drop 0 [1]`` evaluates to ``[1]``


+ ___ / 5: ``rev [1; 2; 3; 4; 5]`` evaluates to ``[5; 4; 3; 2; 1]``

+ ___ / 5: ``rev []`` evaluates to ``[]``



+ ___ / 5: ``is_matrix [ [1;2;3]; [4;5;6] ]`` evaluates to ``true``

+ ___ / 5: ``is_matrix [ [1;2;3]; [4;6] ]`` evaluates to ``false``

+ ___ / 5: ``is_matrix [ [1] ]`` evaluates to ``true``



+ ___ / 7: ``matrix_scalar_add [ [1; 2] ] 5`` evaluates to ``("(6 7)")``

+ ___ / 8: ``matrix_scalar_add [ [1; 2 ;3]; [4; 5; 6] ] 5`` evaluates to ``("(6 7 8)""(9 10 11)")``



