# Homework 3: Introduction to Disjoint Union Types

*CSci 2041: Advanced Programming Principles, Fall 2014*

**Due:** Thursday, September 25 at 5:00pm


## Introduction

This homework builds on the data types and functions that you wrote
for lab 3 and thus you need to complete that before starting on this
work. 


### Setting up files

All functions should be placed in a file named ``hwk_03.ml`` which
resides in a directory named ``hwk_03``.  This directory should be in
a directory named ``homework`` in your GitHub repository.  That is,
you need the path ``homework/hwk_03/hwk_03.ml`` to exist in your repository.

In implementing these functions, do not use any functions from the
``List`` module.  If you need some helper functions over lists, write
them yourself.

Also, you should only use the pure, non-imperative features of OCaml.
No while-loops or references.  But since we've not discussed these
they are easy to avoid.

### Lab 3 material

In lab 3 you designed a type named ``number`` and defined the values
``n1``, ``n2``, ``n4``, ``n5``, and ``n3_1415``.  You also wrote
functions ``to_int`` and ``to_float``.

Copy all of these into your ``hwk_03.ml`` file.



## Additional ``number`` functions

### Maximum

In lab 3 you wrote functions to add, subtract, multiply, and divide
numbers. These functions had the type ``number -> number -> number``.

Write a function called ``max_number`` that returns the maximum value,
as a ``number`` type.  If the maximum number was constructed from an
``int`` (or respectively, a ``float``) then the value that your function
returns should also be constructed from a ``int`` (again, respectively, a
``float``).

For example,
+ ``to_int (max_number n5 n3_1415)`` evaluates to ``Some 5``
+ ``to_float (max_number n2 n3_1415)`` evaluates to ``Some 3.1415``


### Maximum in a list

Now write a function that returns the maximum ``number`` from a list
of ``number`` values, if one exists.  In the case it is given the empty list
then it cannot return a ``number``.

Thus, your function should take as input a ``number list`` and return
as output a ``number option``.  This way it can return an appropriate
value when it is passed the empty list.

For example
+ ``max_number_list [n1; n5; n3_1415]`` should return the second
  element of the list as a ``Some`` value.
+ ``max_number_list []`` should return ``None``.


### Summing differences

Recall the function ``sum_diffs`` from Lab 2 the computed the sum of
the differences of the number in an integer list.

Write a version of that function that works on ``number list`` values
instead and also returns an ``number option`` so that it properly
handles the cases when there are fewer than two values in the list.

To do this, you may want to copy your ``add_number`` and
``sub_number`` functions into this file.

For example
+ ``sum_number_diffs [ n4 ]`` evaluates to ``None``
+ ``sum_number_diffs [ n1; n2; n4; n5; n3_1415]`` evaluates to a
``Some`` value containing the ``number`` representation for -2.1415.




## Assessment
+ ___ / 5: Functions are put into the appropriate file:
           ``homework/hwk_03/hwk_03.ml``.   
+ ____/ 5: Values ``n1``, ``n2``, ``n4``, ``n5``, and ``n3_1415`` are
           appropriately defined.
+ ___ / 5: ``to_int (max_number n5 n3_1415)`` evaluates to ``Some 5``
+ ___ / 5: ``to_float (max_number n2 n3_1415)`` evaluates to ``Some 3.1415``

+ ___ / 5: ``max_number_list [n1; n5; n3_1415]`` should return the second
           element of the list, as a ``Some`` value.
+ ___ / 5: ``max_number_list []`` evaluates to ``None``.


+ ___ / 5: ``sum_number_diffs [ n4 ]`` evaluates to ``None``
+ ___ / 5: ``sum_number_diffs [ n1; n2; n4; n5; n3_1415]`` evaluates to a
           ``Some`` value containing the ``number`` representation for -2.1415.

Additional evaluations of your functions may also be performed.
