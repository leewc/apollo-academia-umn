Below are the results of the initial grading for homework 4, part 2.

The TAs will shortly double check the cases in which a very low score was reported. Thus, if your score is very low and you feel you at least nearly completed the work, please wait for this manual check to be completed.

After this manual process has finished, these lines will be removed and the word "initial" from the first line will be removed. If at that point, there is a grading concern that needs addressing please email **csci2041@cs.umn.edu** with your question or request.

## Scores from homework hwk_04_part_2.ml.

+ 3 / 3: Functions are put into the appropriate file: ``homework/hwk_04/hwk_04_part_2.ml``

    File stored correctly in ``homework/hwk_04//hwk_04_part_2.ml``.


The following functions were used in testing:
```
let remove_spaces s = String.lowercase (String.concat (String.split_on_chars s ~on:[' ']))

let remove_spaces_and_compare s1 s2 = (remove_spaces s1) = (remove_spaces s2)
```
If a test case failed for you, consider copying these functions into your
file and experimenting with them to see what went wrong.


+ 2 / 2: ``eval (Var "x")`` should raise an exception

    Test passed.

+ 2 / 2: ``eval (Let ("x", Var "x", IntConst 1))`` should raise an exception

    Test passed.

+ 2 / 2: ``eval (LT (BoolConst true, BoolConst false))`` should raise an exception

    Test passed.

+ 2 / 2: ``eval (EQ (IntConst 1, BoolConst true))`` should raise an exception

    Test passed.

+ 2 / 2: ``eval (EQ (BoolConst true, IntConst 1))`` should raise an exception

    Test passed.

+ 5 / 5: ``eval (Let ("x", IntConst 1, Var "x"))`` should evaluate to ``IntVal 1``

    Test passed.

+ 5 / 5: ``eval (Let ("x", LT (IntConst 1, IntConst 2), Var "x"))`` should evaluate to ``BoolVal true``

    Test passed.

+ 5 / 5: ``eval (Let ("x", BoolConst true, IntConst 1))`` should evaluate to ``IntVal 1``

    Test passed.

+ 5 / 5: ``eval (Let ("x", IntConst 1, BoolConst true))`` should evaluate to ``BoolVal true``

    Test passed.

+ 5 / 5: ``eval (EQ (IntConst 1, Sub (IntConst 3, IntConst 2)))`` should evaluate to ``BoolVal true``

    Test passed.

+ 5 / 5: ``eval (EQ (LT (IntConst 2, IntConst 1), LT (IntConst 4, IntConst 3)))`` should evaluate to ``BoolVal true``

    Test passed.

+ 5 / 5: ``eval (Let ("x", IntConst 1, Let ("x", IntConst 2, Var "x")))`` should evaluate to ``IntVal 2``

    Test passed.

+ 5 / 5: ``eval (Let ("x", IntConst 2, Let ("x", Add (Var "x", IntConst 1), Var "x")))`` should evaluate to ``IntVal 3``

    Test passed.

+ 5 / 5: ``eval (Not (LT (IntConst 1, IntConst 2)))`` should evaluate to ``BoolVal false``

    Test passed.

+ 5 / 5: ``eval (And (LT (IntConst 1, IntConst 2), LT (IntConst 2, IntConst 1)))`` should evaluate to ``BoolVal false``

    Test passed.

+ 5 / 5: ``eval (IfThenElse (LT (IntConst 1, IntConst 2), IntConst 3, IntConst 4))`` should evaluate to ``IntVal 3``

    Test passed.

+ 5 / 5: ``eval (IfThenElse (LT (IntConst 1, IntConst 2), IntConst 3, Div (IntConst 1, IntConst 0)))`` should evaluate to ``IntVal 3``

    Test passed.

+ 5 / 5: ``eval (IfThenElse (BoolConst true, BoolConst true, BoolConst false))`` should evaluate to ``BoolVal true``

    Test passed.

+ 5 / 5: ``eval (IfThenElse (BoolConst true, BoolConst true, IntConst 1))`` should evaluate to ``BoolVal true``

    Test passed.

+ 4 / 4: ``freevars (IntConst 1)`` should evaluate to ``[]``

    Test passed.

+ 4 / 4: ``freevars (Var "x")`` should evaluate to ``["x"]``

    Test passed.

+ 4 / 4: ``freevars (Add (Var "x", Var "x"))`` should evaluate to ``["x"; "x"]``

    Test passed.

+ 4 / 4: ``freevars (LT (BoolConst true, BoolConst false))`` should evaluate to ``[]``

    Test passed.

+ 4 / 4: ``freevars (Let ("x", IntConst 1, Var "x"))`` should evaluate to ``[]``

    Test passed.

+ 4 / 4: ``freevars (Let ("x", Var "x", IntConst 1))`` should evaluate to ``["x"]``

    Test passed.

+ 4 / 4: ``freevars (And (Not (IntConst 3), IfThenElse (Var "x", IntConst 1, BoolConst true)))`` should evaluate to ``["x"]``

    Test passed.

+ 4 / 4: ``freevars (Let ("c", BoolConst true, Add (Add (Var "a", Var "b"), Add (Var "c", Var "d"))))`` should evaluate to ``["a"; "b"; "d"]``

    Test passed.

+ 8 / 8: ``translate (LT (BoolConst true, BoolConst false))`` should evaluate to ``None``

    Test passed.

+ 8 / 8: ``translate (LT (Add (IntConst 1, IntConst 3), Add (IntConst 2, IntConst 4)))`` should evaluate to ``Some (BoolExpr (LT_bool (Add_int (IntConst_int 1, IntConst_int 3),Add_int (IntConst_int 2, IntConst_int 4))))``

    Test passed.

+ 8 / 8: ``translate (EQ (IntConst 1, IntConst 2))`` should evaluate to ``Some (BoolExpr (EQ_int_bool (IntConst_int 1, IntConst_int 2)))``

    Test passed.

+ 8 / 8: ``translate (EQ (BoolConst true, BoolConst false))`` should evaluate to ``Some (BoolExpr (EQ_bool_bool (BoolConst_bool true, BoolConst_bool false)))``

    Test passed.

+ 8 / 8: ``translate (EQ (IntConst 1, BoolConst true))`` should evaluate to ``None``

    Test passed.

+ 8 / 8: ``translate (EQ (BoolConst true, IntConst 1))`` should evaluate to ``None``

    Test passed.

+ 8 / 8: ``translate (Let ("x", BoolConst true, BoolConst false))`` should evaluate to ``Some (BoolExpr (Let_bool_bool ("x", BoolConst_bool true, BoolConst_bool false)))``

    Test passed.

+ 8 / 8: ``translate (Let ("x", BoolConst true, IntConst 1))`` should evaluate to ``Some (IntExpr (Let_bool_int ("x", BoolConst_bool true, IntConst_int 1)))``

    Test passed.

+ 8 / 8: ``translate (Let ("x", IntConst 1, BoolConst true))`` should evaluate to ``Some (BoolExpr (Let_int_bool ("x", IntConst_int 1, BoolConst_bool true)))``

    Test passed.

+ 8 / 8: ``translate (Let ("x", IntConst 1, IntConst 2))`` should evaluate to ``Some (IntExpr (Let_int_int ("x", IntConst_int 1, IntConst_int 2)))``

    Test passed.

+ 8 / 8: ``translate (IfThenElse (BoolConst true, BoolConst true, BoolConst false))`` should evaluate to ``Some (BoolExpr (IfThenElse_bool (BoolConst_bool true, BoolConst_bool true, BoolConst_bool false)))``

    Test passed.

+ 8 / 8: ``translate (IfThenElse (BoolConst true, IntConst 1, IntConst 2))`` should evaluate to ``Some (IntExpr (IfThenElse_int (BoolConst_bool true, IntConst_int 1, IntConst_int 2)))``

    Test passed.

+ 8 / 8: ``translate (IfThenElse (BoolConst true, BoolConst true, IntConst 1))`` should evaluate to ``None``

    Test passed.

+ 8 / 8: ``translate (IfThenElse (BoolConst true, IntConst 1, BoolConst true))`` should evaluate to ``None``

    Test passed.

+ 8 / 8: ``translate (Div (IntConst 1, IntConst 0))`` should evaluate to ``Some (IntExpr (Div_int (IntConst_int 1, IntConst_int 0)))``

    Test passed.

+ 7 / 7: ``eval_int_bool (BoolExpr (LT_bool (Add_int (IntConst_int 1, IntConst_int 3),Add_int (IntConst_int 2, IntConst_int 4))))`` should evaluate to ``BoolVal true``

    Test passed.

+ 7 / 7: ``eval_int_bool (BoolExpr (EQ_int_bool (IntConst_int 1, IntConst_int 2)))`` should evaluate to ``BoolVal false``

    Test passed.

+ 7 / 7: ``eval_int_bool (BoolExpr (EQ_bool_bool (BoolConst_bool true, BoolConst_bool false)))`` should evaluate to ``BoolVal false``

    Test passed.

+ 7 / 7: ``eval_int_bool (BoolExpr (Let_bool_bool ("x", BoolConst_bool true, BoolConst_bool false)))`` should evaluate to ``BoolVal false``

    Test passed.

+ 7 / 7: ``eval_int_bool (IntExpr (Let_bool_int ("x", BoolConst_bool true, IntConst_int 1)))`` should evaluate to ``IntVal 1``

    Test passed.

+ 7 / 7: ``eval_int_bool (BoolExpr (Let_int_bool ("x", IntConst_int 1, BoolConst_bool true)))`` should evaluate to ``BoolVal true``

    Test passed.

+ 7 / 7: ``eval_int_bool (IntExpr (Let_int_int ("x", IntConst_int 1, IntConst_int 2)))`` should evaluate to ``IntVal 2``

    Test passed.

+ 7 / 7: ``eval_int_bool (BoolExpr (IfThenElse_bool (BoolConst_bool true, BoolConst_bool true, BoolConst_bool false)))`` should evaluate to ``BoolVal true``

    Test passed.

+ 7 / 7: ``eval_int_bool (IntExpr (Div_int (IntConst_int 1, IntConst_int 0)))``should raise an exception

    Test passed.

+ 0 / 7: ``eval_int_bool (IntExpr (IfThenElse_int (BoolConst_bool true, IntConst_int 1, IntConst_int 2)))`` should evaluate to ``IntVal 1``

    Test failed: the expression ``eval_int_bool (IntExpr (IfThenElse_int (BoolConst_bool true, IntConst_int 1, IntConst_int 2))) = IntVal 1`` did not evalaute to as required.

### Total score

+ 298 / 305: total score for this assignment

