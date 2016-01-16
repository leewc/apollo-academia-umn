# Homework 4: Working with expressions as data

*CSci 2041: Advanced Programming Principles, Fall 2014*

**Due:** Wednesday, October 8 at 5:00pm

## Introduction

This homework asks you write a number of functions that implement
computations over expressions and to generate new expressions.

Our goal here is to learn how to work with programs and expressions as
data, to both inspect them, compute values from them, and to construct
them.

### Setting up files

Two files are provided for you ``hwk_04_part_1.ml`` and
``hwk_04_part_2.ml``.  Both of these are in the ``homework/hwk_04``
directory of the public class repository.

Copy these files into a ``hwk_04`` directory in your ``homework``
directory in your individual repository.

When you've finished you will commit and push the files
``homework/hwk_04/hwk_04_part_1.ml`` and
``homework/hwk_04/hwk_04_part_2.ml``.

### Type annontations
For each "top-level" function (those you can call from utop) that you write
include type annontations for the input types and the return type.

## Part 1

Consider the following type for expressions that we've used in class
for a number of examples:
```
type expr 
  = Const of int
  | Add of  expr * expr
  | Mul of expr * expr
  | Sub of expr * expr
  | Div of expr * expr
  | Let of string * expr * expr
  | Var of string
```
This type definition can be found in 
``hwk_04_part_1.ml``

The first part of this assignment will ask you to write two functions
that work over values of this type.


### Converting an expression to a string

Write a function named ``show_expr`` that converts an ``expr`` value
into a ``string`` representation using traditional infix symbols for
the operators.  The output of this function should be something you
could copy and paste into the OCaml interpreter and have it evaluate
to a value.

Addition, multiplication, subtraction, division and let-expressions
should be wrapped in parenthesis so that the generated string
represents the same expression as the input ``expr`` value.  Variables
and constants, however, should not be wrapped in parenthesis.

Your function must include type annotations indicate the types of the
arguments and the return type.


Here are some example evaluations of ``show_expr``:
+ ``show_expr (Add(Const 1, Const 3))`` evaluates to ``"(1+3)"``

+ ``show_expr (Add (Const 1, Mul (Const 3, Const 4)))`` evaluates to ``"(1+(3*4))"``

+ ``show_expr (Mul (Add(Const 1, Const 3),  Div(Const 8, Const 4)))`` evaluates to ``"((1+3)*(8/4))"``

+ ``show_expr (Let ("x", Add(Const 1, Const 3), Mul (Var "x", Div(Const 8, Const 4))))`` evaluates to ``"(let x=(1+3) in (x*(8/4)))"``

If you prefer to have spaces around operators that is OK.  Correctness does not depend on the spaces.

### Converting an expression to a string with minimal parenthesis

While the function ``show_expr`` should create legal expression
strings, they often have extra parenthesis that are not needed to
understand the meaning of the expression.  This
problem asks you to write a similar function named
``show_pretty_expr`` that does not create any unnecessary parenthesis.

Consider the following example using ``show_expr``:
+ ``show_expr (Add (Const 1, Mul (Const 3, Const 4)))`` evaluates to ``"(1+(3*4))"``

The parenthesis around the product "3*4" are not necessary.  Neither
are the parenthesis around the entire expression.

However, in the following case
+ ``show_expr (Mul (Const 4, Add (Const 3, Const 2)))`` evaluates to ``"(4*(3+2))"``

the inner parenthesis around ``3+2`` are needed.  Again, the outer
parenthesis are not needed.  This is because multiplication has higher
precedence than addition.

What about let-expressions?  The "body" of the let expression is
intended to include as much of the expression following the ``in``
keyword as possible, while still respecting any boundaries indicated
by parenthesis.

For example, in
```
let x = 5 in x * 6 + 4
```
the body of the let includes the entire expression ``x * 6 + 4``.
It is *not* the case that, say, this is expression is an addition of a
let expression and the constant 4.

Thus, in the ``show_expr`` result for the following:

+ ``show_expr (Let ("x", Const 5, Add (Mul (Var "x", Const 6), Const 4)))`` evaluates to ``"(let x=5 in ((x*6)+4))"``

all the parenthesis are unnecessary.

But the following does require parenthesis around the let expression.
+ ``show_pretty_expr ( Add (Let ("x", Const 5, Mul (Var "x", Const 6)), Const 4))`` evaluates to ``"(let x=5 in x*6)+4"``


These examples illustrate that an expression needs to be wrapped
in parenthesis if its operator's precedence is lower than the
operator of the expression containing it.

We think of operator precedence as being equal to, lower than,
or higher than the precedence of other operators.  This suggest that
we use integers to represent the precedence of different operators.

We must also consider the associativity of an operation. Consider this
``expr`` value the result of applying ``show_expr`` to it.
+ ``show_expr (Sub (Sub (Const 1, Const 2), Sub (Const 3, Const 4)))`` evaluates to ``"((1-2)-(3-4))"``

Note that since subtraction is left associative (a value between two
subtraction operators is associated with the one to its left) the
parenthesis around ``1-2`` are not needed, but those around ``3-4``
are needed.

All operations represented in our ``expr`` type are left associative.
So when the enclosing operator has the same precedence, it may suffice
for an expression to know if it should be wrapped in parenthesis or
not, by knowing if it is the left child or right child (if either) of
the expression that it is a component of.

Of course in some cases, such as at the root of the expression, it
might not be a component of a binary operator.


Write a function ``show_pretty_expr`` that generates a ``string``
representation of an ``expr`` similar to ``show_expr`` but without any
unnecessary parenthesis.  In doing so, write appropriate helper
functions to avoid an overabundance of copy-and-pasted code fragments
that are non-trivial near exact copies of one another.

Also, be sure to use disjoint union types where appropriate.  While
integers are appropriate for representing precedence of operators,
they may not be appropriate in dealing with issues of associativity.

A few more sample evaluations:
+ ``show_pretty_expr (Add (Const 1, Mul (Const 3, Const 4)))`` evaluates to ``"1+3*4"``

+ ``show_pretty_expr (Add (Mul (Const 1, Const 3), Const 4))`` evaluates to ``"1*3+4"``

+ ``show_pretty_expr (Add (Const 1, Add (Const 3, Const 4)))`` evaluates to ``"1+(3+4)"``

+ ``show_pretty_expr (Add (Add (Const 1, Const 3), Const 4))`` evaluates to ``"1+3+4"``

+ ``show_pretty_expr (Mul (Const 4, Add (Const 3, Const 2)))`` evaluates to ``"4*(3+2)"``

+ ``show_pretty_expr (Let ("x", Const 5, Add (Mul (Var "x", Const 6), Const 4)))`` evaluates to ``"let x=5 in x*6+4"``

+ ``show_pretty_expr (Sub (Sub (Const 1, Const 2), Sub (Const 3, Const 4)))`` evaluates to ``"1-2-(3-4)"``

+ ``show_pretty_expr (Div (Let ("x", Const 1, Var "x"), Let ("y", Const 2, Var "y")))`` evaluates to ``"(let x=1 in x)/let y=2 in y"``

+ ``show_pretty_expr (Add (Add (Let ("x", Const 1, Var "x"), Let ("y", Const 2, Var "y")), Let ("z", Const 3, Var "z")))`` evaluates to ``"(let x=1 in x)+(let y=2 in y)+let z=3 in z"``


## Part 2

In this part, you will be working with a richer notion of
expressions.  Some of the types that are discussed below are provided
for you in the file ``hwk_04_part_2.ml`` described above in the
introduction. 

 The type ``expr`` is extended to the following:
```
type expr 
  = Add of  expr * expr
  | Mul of expr * expr
  | Sub of expr * expr
  | Div of expr * expr
  | Let of string * expr * expr
  | Var of string
  | LT of expr * expr
  | EQ of expr * expr
  | And of expr * expr
  | Not of expr
  | IfThenElse of expr * expr * expr
  | IntConst of int
  | BoolConst of bool
```

This type includes some relational and logical operators that we
discussed in class as well as an if-then-else expression similar to
the one in OCaml.

### Evaluation

For this problem, complete the skeleton implementation of ``eval``
that is provided in ``hwk_04_part_2.ml``.

Keep in mind that the if-then-else, EQ, and let expressions may
evaluate on (or to) either integer or boolean values.

In the case that the expression has an undeclared identifier the
provided ``lookup`` function will raise an exception.

In the case that the expression contains a type error, then your
``eval`` function should raise an exception with an appropriate message -
similar to what is done in the case of ``Add`` as seen in the
skeleton bit of code.  This is duplicated below:
```
let eval (e:expr) : value =
  let rec lookup n env = 
    match env with 
    | [ ] -> raise (Failure ("Identifier \"" ^ n ^ "\" not declared."))
    | (name,value)::rest -> if n = name then value else lookup n rest
  in
  let rec eval_h e env = match e with
    | Add (l,r) -> 
        let v1 = eval_h l env  and  v2 = eval_h r env
        in (match v1,v2 with 
            | IntVal x, IntVal y -> IntVal (x + y)
            | _ -> raise (Failure "Addition requires 2 integer values."))

    | IntConst v -> IntVal v
    | BoolConst b -> BoolVal b

    (* Many cases missing here, you need to complete them. *)

  in eval_h e [ ]
```
Note that the return type of ``eval`` is ``value``, as defined below:
```
type value = IntVal of int | BoolVal of bool
```
Fill in the missing cases to complete the ``eval`` function.

Below are a few sample evaluations:
+ ``eval (Mul (IntConst 4, Add (IntConst 3, IntConst 2)))`` evaluates to ``IntVal 20``

+ ``eval (Let ("lt", LT (IntConst 3, IntConst 4), IfThenElse (Var "lt", Mul (IntConst 4, IntConst 5), Add (IntConst 3, IntConst 2))))`` evaluates to ``IntVal 20``

+ ``eval (Var "x")`` raises exception ``(Failure "Identifier \"x\" not declared.")``

+ ``eval (IfThenElse (LT (IntConst 1, IntConst 2), IntConst 3, Div (IntConst 1, IntConst 0)))`` evaluates to ``IntVal 3``



### Free variables

Write a function named ``freevars`` that takes an ``expr`` value and
returns a list of strings, one string for each occurrence of an
undeclared identifier.

A function such as this has a similar form to ``eval`` above.  Be sure
that any environment or context passed as an argument is appropriate
for this task.

Consider the following definitions of two sample expressions:
```
let e1 = Let ("lt", LT (IntConst 3, IntConst 4),
              IfThenElse (Var "lt", Mul (IntConst 4, IntConst 5),
                          Add (IntConst 3, IntConst 2)))

let e2 = Add (Let ("x", Add (IntConst 3, Var "w"),
                   Add (Var "x", Mul (IntConst 4, Var "w") ) ) ,
              Mul (Let ("y", IntConst 4, Add (IntConst 2, Var "y")),
                   Add (Var "z", IntConst 2)))
```

For ``e1``, the function ``freevars`` should return the empty list.
But for ``e2`` it should return the list ``["w"; "w"; "z"]``.


### Check and translate, then evaluate

The "freevars" function performs a simple kind of name analysis on 
expression to determine if there are any undeclared identifiers.

But we might also like to check that an expression contains no type
errors.  Type checking expressions as simple as those in ``expr`` is
quite simple since there are only two possible basic types.

Expressions that have no undeclared identifiers and also have no type
errors can be translated to a form in which the types for all
expressions have been resolved *before* evaluation.  This would allow
for a more efficient evaluation function than the ``eval`` function
you defined above.  That ``eval`` function checks for type errors
dynamically (as the expression is evaluating) with a ``match``
expression.  As we have discussed, dynamic type checking like this is
a less efficient way to evaluate expressions.  It is better if we can
statically, that is before evaluation, analyze the expression to
detect any undeclared identifiers or type errors and, when there are
none, translate the expression into some other form that can be more
efficiently evaluated.

For this problem, you will write a function ``translate`` that takes
as input an ``expr`` value, resolves the types for all sub-expressions
and when no errors are found, returns a value of type
``int_or_bool_expr`` (wrapped in an ``option``), as defined below:
```
type int_or_bool_expr
  = IntExpr of int_expr 
  | BoolExpr of bool_expr 
```
The types ``int_expr`` and ``bool_expr`` referenced above are defined
in ``hwk_04_part_2.ml``.  These two recursive types have value
constructors that only take ``int_expr`` or ``bool_expr`` expressions
as arguments (except for variables and constants).

Thus, we can only construct values of ``int_expr`` or ``bool_expr``
that do not have any type errors.  This comes with the cost of needing
multiple constructors for expressions that work on both integer and
boolean values.  For example, there are 4 let-expression constructors.
Of course, undeclared identifiers are still possible with this
representation.

Note that there are no value constructors that create an ``int_expr``
or ``bool_expr`` from a vale of type ``int_or_bool_expr``.  There
should not be one.  The ``int_or_bool_expr`` type is use only to "wrap
up" either a ``int_expr`` or a ``bool_expr`` since an expression of
type ``expr`` may be either be a boolean or an integer expression.

In addition to the ``translate`` function you will write an evaluation
function named ``eval_int_bool``.  Since these functions are related
you might think about developing them in tandem, starting with simple
expressions, for example using integer constants and addition, and
progressing to boolean expression and then let-expressions.

#### ``eval_int_bool : int_or_bool_expr -> value`` 

This function evaluates an ``int_or_bool_expr`` expression to compute
its value.  If an undeclared identifier is found, raise an exception.
But since we expect to only provide expressions to ``eval_int_bool``
that were generated by our ``translate`` function, we would not expect
this to happen as ``translate`` would detect this sort of error and
return a value of ``None``.

The only other thing that could go wrong is that a division by 0 may
occur, and we will let the OCaml integer division operator throw and
exception if that happens.

You will need two mutually recursive helper functions, one to evaluate
``int_expr`` expressions and another to evaluate ``bool_expr``
expressions.   Mutually recursive functions are defined as sketched
below:
```
let rec f x =
    ... calls to f and to g ...
    and g y = 
    ... calls to f and to g ...
```
The ``IntVal`` and ``BoolVal`` constructors should each only appear
one time in your ``eval_int_bool`` functions - to wrap up the value
produced by the first call to your helper functions depending on the
type of the expressions in the argument (which has type
``int_or_bool_expr``). 

Since all of the types will be resolved, we can split the environment
into two: one for integer identifies and another for boolean
identifiers. 


#### ``translate : expr -> int_or_bool_expr option``

This function takes an ``expr`` and determines the type (integer or
boolean) for each sub-expression so that it can create return an
``int_expr`` or a ``bool_expr``.

If there is an undeclared variable or a type error in a (sub)
expression, then a value of ``None`` should be returned.  This
indicates that something was wrong with the expression, but tells us
nothing about that error.  While we not like to use a compiler than
only returns ``None`` when there is an error and provides no error
messages, this will do for our purposes.

If there are no statically-determined errors, then ``translate``
returns a ``Some`` value - wrapping up in a ``Some`` either a integer
or boolean expression of type ``int_or_bool_expr``.

Sample evaluations:
+ ``translate (LT (BoolConst true, BoolConst false))`` evaluates to ``None``
+ ``translate (LT (Add (IntConst 1, IntConst 3), Add (IntConst 2, IntConst 4)))`` evaluates to ``Some (BoolExpr (LT_bool (Add_int (IntConst_int 1, IntConst_int 3),Add_int (IntConst_int 2, IntConst_int 4))))``
+ ``eval_int_bool (BoolExpr (LT_bool (Add_int (IntConst_int 1, IntConst_int 3),Add_int (IntConst_int 2, IntConst_int 4))))`` evaluates to ``BoolVal true``


#### Comments

Both of the evaluate and translate functions will follow the same
pattern that we've seen before: a function that calls a nested helper
function, providing it with additional default argument values (such
as an empty environment).

In writing your functions you might consider writing these helper
functions as "top level" functions so that you can call them directly
from "utop".  This will allow you to interact with them more directly
and make it easier to write small test cases to check that they have
the correct behavior.  This also simplifies debugging.




## Assessment
Please keep in mind that lab scores are normalized in computing grades.  
Thus, the high number of points below does not indicate the value of this
lab in computing your grade.

#### Correct file name
+ ___ / 5: Functions are put into the appropriate files:
           ``homework/hwk_04/hwk_04_part_1.ml`` and ``homework/hwk_04/hwk_04_part_2.ml``

#### ``show_expr`` and ``show_pretty_expr``
Your return values, as compared to the below return values, may differ by innocuous spaces. For example, if you got ``"(1 + (2 + 3)) * (4 + 5 + 6)"`` instead of ``"(1+(2+3))*(4+5+6)"``, that is just fine.

+ ___ / 5: ``show_expr (Sub (Let ("x", Add (Const 1, Const 2), Mul (Const 3, Var "x")), Div (Const 4, Const 5)))`` evaluates to ``"((let x=(1+2) in (3*x))-(4/5))"``
+ ___ / 8: ``show_pretty_expr (Mul (Add (Const 1, Add (Const 2, Const 3)), Add (Add (Const 4, Const 5), Const 6)))`` evaluates to ``"(1+(2+3))*(4+5+6)"``
+ ___ / 8: ``show_pretty_expr (Sub (Add (Const 1, Const 2), Const 3))`` evaluates to ``"1+2-3"``
+ ___ / 8: ``show_pretty_expr (Div (Let ("x", Const 1, Var "x"), Let ("y", Const 2, Var "y")))`` evaluates to ``"(let x=1 in x)/let y=2 in y"``
+ ___ / 8: ``show_pretty_expr (Add (Add (Let ("x", Const 1, Var "x"), Let ("y", Const 2, Var "y")), Let ("z", Const 3, Var "z")))`` evaluates to ``"(let x=1 in x)+(let y=2 in y)+let z=3 in z"``
+ ___ / 8: ``show_pretty_expr (Let ("x", Let ("y", Const 1, Var "y"), Let ("z", Var "x", Var "z")))`` evaluates to ``"let x=let y=1 in y in let z=x in z"``
+ ___ / 8: ``show_pretty_expr (Add (Add (Const 1, Const 2), Add (Const 3, Const 4)))`` evaluates to ``"1+2+(3+4)"``
+ ___ / 8: ``show_pretty_expr (Sub (Sub (Const 7, Const 1), Sub (Const 5, Const 2)))`` evaluates to ``"7-1-(5-2)"``

#### ``eval``
+ ___ / 2: ``eval (Var "x")`` raises exception ``(Failure "Identifier \"x\" not declared.")``
+ ___ / 2: ``eval (Let ("x", Var "x", IntConst 1))`` raises exception ``(Failure "Identifier \"x\" not declared.")``
+ ___ / 2: ``eval (LT (BoolConst true, BoolConst false))`` raises exception ``(Failure "Less than operator requires 2 integer values.")``
+ ___ / 2: ``eval (EQ (IntConst 1, BoolConst true))`` raises exception ``(Failure "Equality test requires 2 values of the same type.")``
+ ___ / 2: ``eval (EQ (BoolConst true, IntConst 1))`` raises exception ``(Failure "Equality test requires 2 values of the same type.")``
+ ___ / 5: ``eval (Let ("x", IntConst 1, Var "x"))`` evaluates to ``IntVal 1``
+ ___ / 5: ``eval (Let ("x", LT (IntConst 1, IntConst 2), Var "x"))`` evaluates to ``BoolVal true``
+ ___ / 5: ``eval (Let ("x", BoolConst true, IntConst 1))`` evaluates to ``IntVal 1``
+ ___ / 5: ``eval (Let ("x", IntConst 1, BoolConst true))`` evaluates to ``BoolVal true``
+ ___ / 5: ``eval (EQ (IntConst 1, Sub (IntConst 3, IntConst 2)))`` evaluates to ``BoolVal true``
+ ___ / 5: ``eval (EQ (LT (IntConst 2, IntConst 1), LT (IntConst 4, IntConst 3)))`` evaluates to ``BoolVal true``
+ ___ / 5: ``eval (Let ("x", IntConst 1, Let ("x", IntConst 2, Var "x")))`` evaluates to ``IntVal 2``
+ ___ / 5: ``eval (Let ("x", IntConst 2, Let ("x", Add (Var "x", IntConst 1), Var "x")))`` evaluates to ``IntVal 3``
+ ___ / 5: ``eval (Not (LT (IntConst 1, IntConst 2)))`` evaluates to ``BoolVal false``
+ ___ / 5: ``eval (And (LT (IntConst 1, IntConst 2), LT (IntConst 2, IntConst 1)))`` evaluates to ``BoolVal false``
+ ___ / 5: ``eval (IfThenElse (LT (IntConst 1, IntConst 2), IntConst 3, IntConst 4))`` evaluates to ``IntVal 3``
+ ___ / 5: ``eval (IfThenElse (LT (IntConst 1, IntConst 2), IntConst 3, Div (IntConst 1, IntConst 0)))`` evaluates to ``IntVal 3``
+ ___ / 5: ``eval (IfThenElse (BoolConst true, BoolConst true, BoolConst false))`` evaluates to ``BoolVal true``
+ ___ / 5: ``eval (IfThenElse (BoolConst true, BoolConst true, IntConst 1))`` evaluates to ``BoolVal true``


#### ``freevars``
+ ___ / 4: ``freevars (IntConst 1)`` evaluates to ``[]``
+ ___ / 4: ``freevars (Var "x")`` evaluates to ``["x"]``
+ ___ / 4: ``freevars (Add (Var "x", Var "x"))`` evaluates to ``["x"; "x"]``
+ ___ / 4: ``freevars (LT (BoolConst true, BoolConst false))`` evaluates to ``[]``
+ ___ / 4: ``freevars (Let ("x", IntConst 1, Var "x"))`` evaluates to ``[]``
+ ___ / 4: ``freevars (Let ("x", Var "x", IntConst 1))`` evaluates to ``["x"]``
+ ___ / 4: ``freevars (And (Not (IntConst 3), IfThenElse (Var "x", IntConst 1, BoolConst true)))`` evaluates to ``["x"]``
+ ___ / 4: ``freevars (Let ("c", BoolConst true, Add (Add (Var "a", Var "b"), Add (Var "c", Var "d"))))`` evaluates to ``["a"; "b"; "d"]``

#### ``translate``
+ ___ / 8: ``translate (LT (BoolConst true, BoolConst false))`` evaluates to ``None``
+ ___ / 8: ``translate (LT (Add (IntConst 1, IntConst 3), Add (IntConst 2, IntConst 4)))`` evaluates to ``Some (BoolExpr (LT_bool (Add_int (IntConst_int 1, IntConst_int 3),Add_int (IntConst_int 2, IntConst_int 4))))``
+ ___ / 8: ``translate (EQ (IntConst 1, IntConst 2))`` evaluates to ``Some (BoolExpr (EQ_int_bool (IntConst_int 1, IntConst_int 2)))``
+ ___ / 8: ``translate (EQ (BoolConst true, BoolConst false))`` evaluates to ``Some (BoolExpr (EQ_bool_bool (BoolConst_bool true, BoolConst_bool false)))``
+ ___ / 8: ``translate (EQ (IntConst 1, BoolConst true))`` evaluates to ``None``
+ ___ / 8: ``translate (EQ (BoolConst true, IntConst 1))`` evaluates to ``None``
+ ___ / 8: ``translate (Let ("x", BoolConst true, BoolConst false))`` evaluates to ``Some (BoolExpr (Let_bool_bool ("x", BoolConst_bool true, BoolConst_bool false)))``
+ ___ / 8: ``translate (Let ("x", BoolConst true, IntConst 1))`` evaluates to ``Some (IntExpr (Let_bool_int ("x", BoolConst_bool true, IntConst_int 1)))``
+ ___ / 8: ``translate (Let ("x", IntConst 1, BoolConst true))`` evaluates to ``Some (BoolExpr (Let_int_bool ("x", IntConst_int 1, BoolConst_bool true)))``
+ ___ / 8: ``translate (Let ("x", IntConst 1, IntConst 2))`` evaluates to ``Some (IntExpr (Let_int_int ("x", IntConst_int 1, IntConst_int 2)))``
+ ___ / 8: ``translate (IfThenElse (BoolConst true, BoolConst true, BoolConst false))`` evaluates to ``Some (BoolExpr (IfThenElse_bool (BoolConst_bool true, BoolConst_bool true, BoolConst_bool false)))``
+ ___ / 8: ``translate (IfThenElse (BoolConst true, IntConst 1, IntConst 2))`` evaluates to ``Some (IntExpr (IfThenElse_int (BoolConst_bool true, IntConst_int 1, IntConst_int 2)))``
+ ___ / 8: ``translate (IfThenElse (BoolConst true, BoolConst true, IntConst 1))`` evaluates to ``None``
+ ___ / 8: ``translate (IfThenElse (BoolConst true, IntConst 1, BoolConst true))`` evaluates to ``None``
+ ___ / 8: ``translate (Div (IntConst 1, IntConst 0))`` evaluates to ``Some (IntExpr (Div_int (IntConst_int 1, IntConst_int 0)))``

#### ``eval_int_bool``
+ ___ / 7: ``eval_int_bool (BoolExpr (LT_bool (Add_int (IntConst_int 1, IntConst_int 3),Add_int (IntConst_int 2, IntConst_int 4))))`` evaluates to ``BoolVal true``
+ ___ / 7: ``eval_int_bool (BoolExpr (EQ_int_bool (IntConst_int 1, IntConst_int 2)))`` evaluates to ``BoolVal false``
+ ___ / 7: ``eval_int_bool (BoolExpr (EQ_bool_bool (BoolConst_bool true, BoolConst_bool false)))`` evaluates to ``BoolVal false``
+ ___ / 7: ``eval_int_bool (BoolExpr (Let_bool_bool ("x", BoolConst_bool true, BoolConst_bool false)))`` evaluates to ``BoolVal false``
+ ___ / 7: ``eval_int_bool (IntExpr (Let_bool_int ("x", BoolConst_bool true, IntConst_int 1)))`` evaluates to ``IntVal 1``
+ ___ / 7: ``eval_int_bool (BoolExpr (Let_int_bool ("x", IntConst_int 1, BoolConst_bool true)))`` evaluates to ``BoolVal true``
+ ___ / 7: ``eval_int_bool (IntExpr (Let_int_int ("x", IntConst_int 1, IntConst_int 2)))`` evaluates to ``IntVal 2``
+ ___ / 7: ``eval_int_bool (BoolExpr (IfThenElse_bool (BoolConst_bool true, BoolConst_bool true, BoolConst_bool false)))`` evaluates to ``BoolVal true``
+ ___ / 7: ``eval_int_bool (IntExpr (Div_int (IntConst_int 1, IntConst_int 0)))`` raises exception ``Division_by_zero``
+ ___ / 7: ``eval_int_bool (IntExpr (IfThenElse_int (BoolConst_bool true, IntConst_int 1, IntConst_int 2)))`` evaluates to ``IntVal 1``

Additional evaluations of your functions may also be performed.
