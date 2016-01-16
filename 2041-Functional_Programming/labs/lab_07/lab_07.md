# Lab 7 - Improving the quality of OCaml pattern matching functions

*CSci 2041: Advanced Programming Principles, Fall 2014*

**Due** Friday, October 24, 5:00pm


## Introduction 

Copy the contents of your homework 4 part 2 solutions into a file
named ``lab_07.ml`` and place this file in a ``lab_07`` directory in
your ``labs`` directory in your individual repository.

**Note:** Homework 4 files will not be examined in evaluating your
  work on this lab.  If you did not complete homework 4 and are
  expecting this lab to reflect work you did after that due date, then
  that work must appear in this ``lab_07.ml`` file.


### Working in pairs

If you are working in pairs at a computer, then you should split your time into 25 minutes
time slots, each person taking a turn at the keyboard.  The person typing snould work
on their solution to this lab, but is free to discuss how to do this with their partner.
When the second person takes over, work on a part of the lab that the pair of you did
not cover in the first 25 minutes.  This will give both of you a chance to discuss how best
to solve the problem in this lab.


## Possible improvements to your previous work

Below are a number of tips and techniques that can help to improve
your OCaml programs.

Apply each one.  You may find that several of these apply to your code
and that you will want to apply them all in one rewrite of a particular
function.  Thus, be sure to read over the entire lab before starting
to work.

If you've already written your homework 4 so that it does all of these
things, then all you need to do is copy that work in to the new
``lab_07.ml`` file mentioned above.


### Several patterns in one clause

It is sometimes the case that the same expression appears in several
different clauses of a ``match`` expression.

Take a look at your ``freevars`` implementation from Homework 4 to see
if this is the case there.

You might find that you have the same expression for the ``Add`` case
as the ``Mul`` case if you named the pattern variables the same.

OCaml lets you avoid this by having multiple patterns for the same
clause. For this to work, each pattern must introduce the same pattern
variables with the same types.  This allows OCaml to statically check
the types of the pattern variables used in the expression part of the
clause.

To see an example of this consider the following function
``count_lets`` of type ``expr -> int`` that counts the number of
let-expressions in an expression.
```
let rec count_lets (e:expr) : int = 
  match e with
  | Add (l,r) | Mul (l,r) | Sub (l,r) | Div (l,r)
  | LT (l,r)  
  | EQ(l,r)   
  | And (l,r) -> count_lets l + count_lets r

  | Let (_,e1,e2) -> 1 + count_lets e1 + count_lets e2
  | Var var -> 0

  | Not l -> count_lets l
  | IfThenElse (c,l,r) -> count_lets c + count_lets l + count_lets r
  
  | IntConst _ -> 0
  | BoolConst _ -> 0
```

The first clause of this ``match`` has a compound pattern made up of 7
simple patterns.  Here we can read the vertical bar ``|`` as "or" in
checking to see if the clause should be matched.

We could write each "sub" pattern on the same line, as we did for the
four arithmetic operator constructors, or on separate lines as we did
for the others.

Each pattern must introduce the same set of variables with the same types.
Notice that each pattern introduces the same pattern variables ``l``
and ``r`` of type ``expr``.  We could not, for example, include the
pattern ``Not l`` here since it doesn't introduce ``r``.

Modify your ``freevars`` function to make use of this technique. 



### Using pattern matching on pairs

Look again at the sample portions of ``eval`` that were provided for
homework 4.  Notice how pattern matching is used on a pair
(``(v1,v2)``) in the inner match inside the ``Add`` case.

This is a common pattern and one that should be applied throughout
your implementation of ``eval``, ``translate``, and
``eval_int_bool``.  If you don't currently follow this pattern, then
modify your implementations to do so.


### Use pattern matching instead of ``if-then-else`` expressions

A common mistake in functional programs written by beginners is the use of
``if-then-else`` expressions when a ``match`` expression would be a
better choice.  This is especially the case when the **nested**
``if-then-else`` expressions are used.

You should be able to implement ``eval`` and ``eval_int_bool`` by
using OCaml ``if-then-else`` expressions **only** in your "lookup" function
for getting values out of the environment and for evaluating the
``IfThenElse`` constructor in ``eval`` and the ``IfThenElse_int`` and
``IfThenElse_bool`` constructors in ``eval_int_bool``.  For
``translate`` you should only need an ``if-then-else`` expression in
your "lookup" function.

If you use ``if-then-else`` expressions elsewhere in ``eval``,
``translate``, or ``eval_int_bool`` then rewrite your code to make
better use of pattern matching to remove them.


### Translate

Functional programs should also be efficient.  In the case of
``translate`` there should be only one traversal of the ``expr`` value
to either compute the translation to an ``expr_int_bool`` value or
determine that there is a static error (an undeclared name or a type
error).

Thus, you should **not** call ``freevars`` to determine if there are
any undeclared names in the program.  If there are, then this should
be detected in the analysis of an expression constructed by the
``Var`` constructor.  In this case, ``translate`` will simply return
``None``. 

Similarly, you should **not** call a function that computes the type
of an expression to determine if there are any type errors.  Type
errors should be detected by translate as it performs the single
traversal of the input expression.




### Descriptive names

Good code uses descriptive names, both for top-level values visible to users
of the code and for internal names that are only seen by those reading
the source code.

Make sure that the names you use are descriptive.  For example, in the
case of ``eval_int_bool`` you may have two mutually recursive helper
functions for carrying out the evaluation.  Do not name these
something short and meaningless like ``f`` and ``g``.

For guidlines regarding variable naming refer to [the Caml Programming Guidelines](http://caml.inria.fr/resources/doc/guides/guidelines.en.html).
There is a sub-section named "How to Choose Identifiers".
In general, when in doubt about how to style your code, follow this guidelines recommendation.


### Type annotations

Type annotations help readers to more easily understand programs than
when they have to infer the types themselves.

Thus, add type annotations to all top-level functions: ``freevars``,
``eval``, ``translate``, and ``eval_int_bool``.



### Extra Credit

The function ``translate`` returns very little feedback in the case
that the input expression has some sort of static error.

Create a new version, called ``translate_report_errors`` that replaces
the return type ``expr_int_bool option`` from ``translate`` with some
kind of type that allows correct expressions to be returned but also
allows a list of error messages to be returned.  This type should be a
disjoint union type where each possible outcome (correct expression or
list of errors) corresponds to a value constructor in the type.

Provide 4 or 5 sample expressions that show how your new translate
function detects errors and returns a reasonable list of error
messages.

If an expression contains more than one error, your function should
make mention of all of them.

Of course, the quality of these messages will be limited because we
cannot match sub-expressions with some line and column from an input
text.  So error messages that describe the error but don't indicate
where it occurred are OK.

Of course, if you can think of a nice way to provide some sort of
location information in the error messages, then do so.




## Assessment

+ ___ / 5: Functions are put into the appropriate file:
           ``labs/lab_07/lab_07.ml``


+ ___ / 15: Appropriate use of multiple patterns in a single clause
in ``freevars``.

+ ___ / 15: Pattern matching is used appropriately. It is applied to
pairs of values where useful, and ``if-then-else`` expressions are
avoided. 

+ ___ / 15: The ``translate`` function makes just one pass over the
``expr`` input and therefore does not call ``freevars`` or any sort of
"get-type" function.

+ ___ / 10: Descriptive names are used throughout the function
implementations. 

+ ___ / 10: Type annotations are provided on all top-level functions
``freevars``, ``eval``, ``translate``, and ``eval_int_bool``.

+ ___ / 10: A new version of ``translate``, named
``translate_report_errors``, is implemented following all the
guidelines discussed in this lab and it incorporates the specified
improvements to ``translate``.
