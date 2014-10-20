## Scores from homework hwk_03.ml.

+ 5 / 5: Functions are put into the appropriate file: ``homework/hwk_03/hwk_03.ml``

    File stored correctly in ``homework/hwk_03//hwk_03.ml``.

+ 1 / 1: Defined n1 appropriately

    Test passed.

+ 1 / 1: Defined n2 appropriately

    Test passed.

+ 1 / 1: Defined n4 appropriately

    Test passed.

+ 1 / 1: Defined n5 appropriately

    Test passed.

+ 1 / 1: Defined n3_1415 appropriately

    Test passed.

+ 5 / 5: ``to_int (max_number n5 n3_1415)`` evaluates to ``Some 5``

    Test passed.

+ 5 / 5: ``to_float (max_number n2 n3_1415)`` evaluates to ``Some 3.1415``

    Test passed.

+ 5 / 5: ``max_number_list [n1; n5; n3_1415]`` should return the second element of the list, as a ``Some`` value.

    Test passed.

+ 5 / 5: ``max_number_list []`` evaluates to ``None``.

    Test passed.

+ 0 / 5: ``sum_number_diffs [ n4 ]`` evaluates to ``None``

    Test failed: the expression ``sum_number_diffs [ n4 ]=None`` could not be evaluated. A syntax or type error occurred.

+ 0 / 5: ``sum_number_diffs [ n1; n2; n4; n5; n3_1415]`` evaluates to a ``Some`` value containing the ``number`` representation for -2.1415.

    Test failed: the expression ``(match (match (sum_number_diffs [ n1; n2; n4; n5; n3_1415]) with | Some y -> to_float y | _ -> None) with | Some x -> x<(-2.1315000000000004) && x>(-2.1515) | None -> false)`` could not be evaluated. A syntax or type error occurred.

### Total score

+ 30 / 40: total score for this assignment

