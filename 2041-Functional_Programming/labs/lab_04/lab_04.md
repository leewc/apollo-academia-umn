# Lab 4: Thinking With Types

*CSci 2041: Advanced Programming Principles, Fall 2014*

**Due:** Friday, September 26 at 5:00pm.  You should be able to
complete lab work during the lab.   But occasionally some work may not
get completed, thus this due date. 

# Introduction

### Goals of this lab: Thinking With Types

OCaml and Haskell both support *type inference*.  Type inference
allows you to not write down the types for the identifiers in your
programs; instead the type system figures out their types based on how
they are used.  These *inferred* types are then checked to ensure that
no type errors exist.

This is often touted as a nice feature of these languages.

*However, just because you do not need to write down the types does not
mean that you should not be thinking about types when you write your
programs.*

*The first step in writing a function should be in determining
 precisely what the types of the input and the output should be.*

The real benefit of type inference is that you don't have to write down
types *everywhere*, but it is wise and good practice to write them down
for the primary functions that one is developing.  Leaving types to be
inferred for helper functions or temporary values where the type is
clear is rather convenient.

Writing down the types you want also helps the compiler to sometimes
give more helpful error messages.  

This lab will show you a few ways to write down types so that they
will become explicit in your thinking when writing programs.

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

Make a directory named *lab_04* and change into it:
```
% mkdir lab_04
% cd lab_04
```

*New* Copy your completed *lab_03.ml* file to a file named *lab_04.ml*
in your *lab_04* directory
```
% cp ../lab_03/lab_03.ml lab_04.ml
```

It is in this file that you will put your solutions to the programming 
problems below.

# Thinking With Types

### Writing types in comments

Open up *lab_04.ml* in your favorite editor.
For each function defined in your lab, write a comment above its
definition that gives the OCaml type for that function. In the comment,
also write a sentence or two indicating what the function does.

Load *lab_04.ml* into OCaml/utop and verify that the types in your
comments matches what OCaml infers for them.

### Writing types in OCaml

OCaml lets you specify what the intended types are for the values that
you define.  The colon ``:`` can be read as "has type".

For example, consider these definitions
```
let i:int = 4
let inc (x:int) :int = x + 1
let add (x:int) (y:int) :int = x + y
```
Thus, the first definition can be read as "let i have type integer and
value 4."

Note function parameters can be annotated with their types, but they
must be wrapped in parentheses.  The return type of the function is
separated from the arguments. The parentheses around parameters with
type annotations are to distinguish the type annotations on
arguments from the type annotation specifying the return type.

To see this, consider the following correct, but hard to read,
function definition
```
let strange x:float = float (x+1)
```
Here, OCaml interprets the ``:float`` as the return type of the
function, which is correct.  But visually, one may think that the
``x`` parameter is given type ``float``.

Thus, if one writes type annotations, it is wise to provide type
annotations for all parameters and the return type.  We could rewrite
the above as the following easier to read definition:
```
let better (x:int) :float = float (x+1)
```

If one uses ``function``  in writing functions that pattern match on
their argument then the parameter name is not provided and thus we
cannot provide an annotation for it.  But we can still write the type
of the function.   Consider the example below:
```
type color = Red | Green | Yellow

let meaning:color->string = function
  | Red -> "Stop"
  | Green -> "Go"
  | Yellow -> "Hit the gas!"
```
Here we've given the function type, as reported by OCaml, of the
function ``meaning``.  In the example of ``add`` above, the argument
and return types are specified and from this one can figure out the
type of the function being declared even though no ``->`` notations
are used.


#### Adding type annotations

In your ``lab_04.ml`` file, write type annotations for all of your
functions: ``to_int``, ``to_float``, ``add_number``, ``sub_number``,
``mul_number``, ``div_number``.

If your implementation of ``to_int`` or ``to_float`` did not use
``function`` in the definition, then rewrite them so that they do.
Then provide the functional type annotation for each one.


Load *lab_04.ml* into OCaml/utop and verify that the types you've
specified are correct.  OCaml will give an error if the specified types
are not correct.

### Pattern matching, revisited

Pattern matching in OCaml and Haskell is quite general.  One can match
over expressions of primitive types such as integers and strings, as
well as over structured types such as ``number`` from lab 3.  One can
also match over tuples.

While matching over tuples might not immediately seem especially
useful, they can often simplify problems where one needs to compare 2
or more pieces of data.

In your functions for adding numbers from lab 3, such as
``add_number`` you needed to determine if each number was constructed
from an integer or a floating point value so that the operation could
be carried out appropriately.

Consider the following function that tests if two ``number`` values are 
both positive.  (Note that here ``IntVal`` and ``FloatVal`` are used as
the names of value constructors.  Your solution may have picked different
names.)
```
let both_positive n1 n2 =
  match (n1, n2) with
  | (IntVal i1, IntVal i2) -> i1 > 0 && i2 > 0
  | (IntVal i1, FloatVal f2) -> i1 > 0 && f2 > 0.0
  | (FloatVal f1, IntVal i2) -> f1 > 0.0 && i2 > 0
  | (FloatVal f1, FloatVal f2) -> f1 > 0.0 && f2 > 0.0
```
To be fair, we could have written a single ``is_positive`` function of type ``number->bool`` 
and just called that funcion on ``n1`` and ``n2``.  But this implementation demonstrates
how matching on tuples works.

Using this on functions like ``add_number`` means that we can avoid writing nested
``match`` expressions.  These nested ``match`` expressions 
can make the code less easy to read
but also opens up the possibility of errors creeping in if the inner ``match`` expressions
are not nested in parentheses.

If you used nested ``match`` expressions in your solution to ``add_number`` in lab 3, then rewrite
it to match on pairs of ``number`` values instead.

Does this version seem easier to write and read?

The point here is that pattern matching can be used in more interesting ways than
simply matching on each constructor for a disjoint union.  Techniques like
the one above can simpify our code and are possible because the language 
supports a general notion of pattern matching and has tuples as a type of data that are 
easy to use and create.




### Sometime soon ...

*utop* is now installed on the CSE systems.   To make all of the demos that
are done in lecture work for you, you need to create a file called
``.ocamlinit`` (note the dot in the name) that is placed in your home
directory.  

Go to your home directory:
```
% cd
```
and then create this file and copy and paste the following lines into it:
```
#use "topfind";;
#thread;;
#camlp4o;;
#require "core.top";;
(* #require "core.syntax";;  *)

open Core.Std
```



# Assessment
Lab 04 work is assessed as follows:
+  __ / 5:  Attended the lab session.
+  __ / 5:  Successfully committed the file ``lab_04/lab_04.ml`` to ``labs`' directory.

+ ___ / 3: A comment with the correct type for ``add_number``
+ ___ / 2: A comment with a description of the intent for ``add_number``

+ ___ / 3: A comment with the correct type for ``sub_number``
+ ___ / 2: A comment with a description of the intent for ``sub_number``

+ ___ / 3: A comment with the correct type for ``mul_number``
+ ___ / 2: A comment with a description of the intent for ``mul_number``

+ ___ / 3: A comment with the correct type for ``div_number``
+ ___ / 2: A comment with a description of the intent for ``div_number``

+ ___ / 3: A comment with the correct type for ``to_int``
+ ___ / 2: A comment with a description of the intent for ``to_int``

+ ___ / 3: A comment with the correct type for ``to_float``
+ ___ / 2: A comment with a description of the intent for ``to_float``

+ ___ / 5: The correct type annotation is given in the definition of
           ``add_number``
+ ___ / 5: The correct type annotation is given in the definition of
           ``sub_number``
+ ___ / 5: The correct type annotation is given in the definition of
           ``mul_number``
+ ___ / 5: The correct type annotation is given in the definition of
           ``div_number``

+ ___ / 2: ``to_int`` is written using ``function`` notation
+ ___ / 3: ``to_int`` has the correct type annotation.
+ ___ / 2: ``to_float`` is written using ``function`` notation
+ ___ / 3: ``to_float`` has the correct type annotation.

+ ___ / 10: Convert ``add_number`` to use pattern matching on pairs instead of using
            nested ``match`` expressions.
+ ___ / 5: Make sure it still works.  Check that 
           ``to_float (add_number n2 n3_1415)`` evaluates to ``Some 5.1415``


**Due:** Friday, September 26 at 5:00pm.  You should be able to
complete lab work during the lab.  But occasionally some work may not
get completed, thus this due date.

Note that these changes must exist in your repository on
github.umn.edu.  Doing the work, but failing to push those changes to
your central repository cannot be assessed.
