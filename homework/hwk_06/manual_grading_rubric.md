# Deductions from automatic grading scores.

These deductions are made if points were awarded by the automatic grading scripts but the
functions do not follow the instructions.  The deductions will not exceed the amount of
points awarded by the grading script.

+ ?? / (-11) Deduction if ``is_elem`` is written as a recursive function or relies on a recursive function 
        other than ``map``, ``filter``, ``foldl``, ``foldr``, ``take``, or ``drop``.

+ ?? / (-11) Deduction if ``length`` is written as a recursive function or relies on a recursive function 
        other than ``map``, ``filter``, ``foldl``, ``foldr``, ``take``, or ``drop``.

+ ?? / (-30) Deduction if ``split_by`` is written as a recursive function or relies on a recursive function 
        other than ``map``, ``filter``, ``foldl``, ``foldr``, ``take``, ``drop``, or ``is_elem``.

+ ?? / (-30) Deduction if ``convert_to_non_blank_lines_of_words`` is written as a recursive function or relies on a recursive function 
        other than ``map``, ``filter``, ``foldl``, ``foldr``, ``take``, ``drop``, ``length``, ``is_elem``, or ``split_by``


# Programming style 

+ ?? / 5 type annontation or comment for ``is_elem`` is accurate for the function as written

+ ?? / 5 type annontation or comment for ``split_by`` is accurate for the function as written

+ ?? / 5 useful comment describing behavior of ``split_by``

+ ?? / 5 type of ``split_by`` is stated in comment or annotations as being
        ``('b -> 'a -> bool) -> 'a list -> 'b list -> 'a list list``

+ ?? / 5 type of ``split_by`` is inferred by OCaml as being
        ``('b -> 'a -> bool) -> 'a list -> 'b list -> 'a list list``

+ ?? / 5 type annontation or comment for ``length`` is accurate for the function as written

+ ?? / 5 type annontation or comment for ``convert_to_non_blank_lines_of_words`` 
        is accurate for the function as written

