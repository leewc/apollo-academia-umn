# Lab 3: Introduction to Disjoint Unions

*CSci 2041: Advanced Programming Principles, Fall 2014*

**Due:** Friday, September 19 at 5:00pm.  You should be able to
complete lab work during the lab.   But occasionally some work may not
get completed, thus this due date. 

# Introduction

### Goals of this lab:

In this lab you will design a simple disjoint union types to define a
number type that includes integers and floating point numbers.

### Working together:

+ You are encouraged to work in pairs and help one another solve the
small programming problems posed below.  You must submit your work
individually, but it is OK if it was done jointly.  If you aren't working 
with a partner at your computer, then discuss the problems with your
neighbors.  Collaboration on labs is encouraged!  (Homework, not so
much...)

+ If there are two people at your computer then after 25 minutes, 
let the person who has not been doing most of the typing have a turn 
operating the keyboard.

# Getting started.

In your individual repository, change into the *labs* directory.
```
% cd labs
```

Make a directory named *lab_03* and change into it:
```
% mkdir lab_03
% cd lab_03
```

Create an empty file with the name *lab_03.ml*:
```
% touch lab_03.ml
```

It is in this file that you will put your solutions to the programming 
problems below.

# Investigating disjoint union types


### Recall the option type

Recall the following type provided in the OCaml libraries.
```
type 'a option = None  |  Some of 'a
```

Be sure you understand how to use this type, how to create values of
this type, and how to inspect values of this type using pattern
matching.  If you are not familiar with how ``option`` works, speak to
your fellow students or TA before continuing.

### A disjoint union type for numbers

Your task is to define an disjoint union called ``number`` and a
collection of supporting functions.  You may need to read ahead in
this document to understand how to design this new type.

Your ``number`` type must support the union of integers and floating
point numbers.  We will want to support various arithmetic operations
over this type that choose the most appropriate representation (that
is, the appropriate value constructor case in ``number``).

To some extent, your ``number`` type will behave like the ``int`` and
``float`` types in languages like C and Java.  In these languages,
there are automatic conversions from integers to floats.  For example
1 + 3.14 is the addition of an integer number to a float number and it
results in a float number.  When we define ``add_number`` below it
will have similar behavior.

Thus, your ``number`` type must include a value constructor that takes
an OCaml ``int`` as its value, and another value constructor that
takes an OCaml ``float`` as its value.


### Some numeric constants

Using a ``let`` declaration, declare a value named ``n1`` of type
``number`` that holds the integer value 1.

Using a ``let`` declaration, declare a value named ``n2`` of type
``number`` that holds the integer value 2.


Using a ``let`` declaration, declare a value named ``n4`` of type
``number`` that holds the integer value 4.

Using a ``let`` declaration, declare a value named ``n5`` of type
``number`` that holds the integer value 5.


Using a ``let`` declaration, declare a value named ``n3_1415`` of type
``number`` that holds the floating point value 3.1415.

Consider the functions below; they may give you some guidance on
creating this type.

### Converting numbers to primitive types

To perhaps clarify the intention of your ``number`` type, write a
function called ``to_int`` with the type ``number -> int option``.
This function attempts to extract an integer value from a number if
that number was constructed from an integer.  If it was, then a
``Some`` value is returned, otherwise the value ``None``.

For example
+ ``to_int n1`` evaluates to ``Some 1``
+ ``to_int n2`` evaluates to ``Some 2``
+ ``to_int n3_1415`` evaluates to ``None``

Also, write a function called ``to_float`` with the type ``number ->
float option`` that behaves similarly, but for floats.

For example
+ ``to_float n1`` evaluates to ``None``
+ ``to_float n2`` evaluates to ``None``
+ ``to_float n3_1415`` evaluates to ``Some 3.1415``  


### Addition

Now that you know how to inspect values of type ``number`` write a
function to add these types of values.  This function should be named
``add_number`` and have the type ``number -> number -> number``.

When both arguments to ``add_number`` were constructed from integers
then their sum must also be constructed from an integer.  Otherwise
the result should be constructed from a float.

Consider these example evaluations
+ ``to_int (add_number n1 n2)`` evaluates to ``Some 3``
+ ``to_int (add_number n2 n3_1415)`` evaluates to ``None``
+ ``to_float (add_number n2 n3_1415)`` evaluates to ``Some 5.1415``

### Subtraction and Multiplication

Now that you have an addition function, write functions ``sub_number``
and ``mul_number``. These functions have the same type as
``add_number`` and are quite similar to it.

Each of these three functions determines the value constructor to be
used in constructing the result based on the value constructors used
to construct the two arguments.

### Division

Now, define ``div_number``, also of type ``number -> number ->
number``.  This function is similar to the previous three that you
have defined, but it is different in one important aspect.

Unlike the previous three functions, this one determines the value
constructor to be used in constructing the result based not only on
the value constructors used to construct the two arguments but also
the values provided to these value constructors.

For example:
+ ``to_int (div_number n4 n2)`` evaluates to ``Some 2`` while
+  ``to_int (div_number n5 n2)`` evaluates to ``None`` and
+  ``to_float (div_number n5 n2)`` evaluates to ``Some 2.5``

Notice that when "integer" values are divided the constructor used to
construct the ``number`` type takes an integer value if the first is
divisible by the second, and it takes a floating point value if it is
not.

This concludes Lab 3.  Homework 3 will be posted sometime later this
afternoon.


# Assessment
Lab 03 work is assessed as follows:
+  __ / 5:  Attended the lab session.
+  __ / 5:  Successfully committed the file ``lab_03/lab_03.ml`` to ``labs`' directory.

+ ___ / 2: define ``n1`` as the value specified above
+ ___ / 2: define ``n2`` as the value specified above
+ ___ / 2: define ``n4`` as the value specified above
+ ___ / 2: define ``n5`` as the value specified above
+ ___ / 2: define ``n3_1415`` as the value specified above

+ ___ / 2: ``to_int n1`` evaluates to ``Some 1``
+ ___ / 2: ``to_int n2`` evaluates to ``Some 2``
+ ___ / 2: ``to_int n3_1415`` evaluates to ``None``

+ ___ / 2: ``to_float n1`` evaluates to ``None``
+ ___ / 2: ``to_float n2`` evaluates to ``None``
+ ___ / 2: ``to_float n3_1415`` evaluates to ``Some 3.1415``  

+ ___ / 2: ``to_int (add_number n1 n2)`` evaluates to ``Some 3``
+ ___ / 2: ``to_int (add_number n2 n3_1415)`` evaluates to ``None``
+ ___ / 2: ``to_float (add_number n2 n3_1415)`` evaluates to ``Some 5.1415``

+ ___ / 2: ``to_int (sub_number n4 n2)`` evaluates to ``Some 2``
+ ___ / 2: ``to_int (sub_number n5 n3_1415)`` evaluates to ``None``
+ ___ / 2: ``to_float (sub_number n5 n3_1415)`` evaluates to ``Some 1.8585``

+ ___ / 2: ``to_int (mul_number n4 n2)`` evaluates to ``Some 8``
+ ___ / 2: ``to_int (mul_number n2 n3_1415)`` evaluates to ``None``
+ ___ / 2: ``to_float (mul_number n2 n3_1415)`` evaluates to ``Some 6.283``

+ ___ / 2: ``to_int (mul_number n4 n2)`` evaluates to ``Some 8``
+ ___ / 2: ``to_int (mul_number n2 n3_1415)`` evaluates to ``None``
+ ___ / 2: ``to_float (mul_number n2 n3_1415)`` evaluates to ``Some 6.283``

+ ___ / 2: ``to_int (div_number n4 n2)`` evaluates to ``Some 2``
+ ___ / 2: ``to_int (div_number n5 n2)`` evaluates to ``None``
+ ___ / 2: ``to_int (div_number n5 n3_1415)`` evaluates to ``None``
+ ___ / 2: ``to_float (div_number n5 n3_1415)`` evaluates to (approximately)
``Some 1.59159``



**Due:** Friday, September 19 at 5:00pm.  You should be able to
complete lab work during the lab.  But occasionally some work may not
get completed, thus this due date.

Note that these changes must exist in your repository on
github.umn.edu.  Doing the work, but failing to push those changes to
your central repository cannot be assessed.

