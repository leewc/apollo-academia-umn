UPDATE to hwk4 part 2 assessments. 

The last test case had an error, so disregard the last one in your part-2 grading file.  Your total score for this assignment will be the scores in the other two assessment files and the test case in this one, which correctly grades the last test.  Below, disregard the total and the score for correctly naming the file.

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


+ 7 / 7: ``eval_int_bool (IntExpr (IfThenElse_int (BoolConst_bool true, IntConst_int 1, IntConst_int 2)))`` should evaluate to ``IntVal 1``

    Test passed.

### Total score

+ 10 / 10: total score for this assignment

