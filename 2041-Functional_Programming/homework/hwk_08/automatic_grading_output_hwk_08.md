## Scores from homework hwk_08.ml.

+ 5 / 5: Assignment has been placed in file named  ``homework/hwk_08/hwk_08.ml``.

    File stored correctly in ``homework/hwk_08/hwk_08.ml``.

+ 15 / 15: The ``file hwk_08.ml`` has no errors and no failing assertions.

    File compiled successfully.

+ 10 / 10: ``take 5 (squares_from 3)`` should evaluate to  ``[9; 16; 25; 36; 49]``

    Test passed.

+ 10 / 10: ``take 5 squares_again`` should evaluate to  ``[1; 4; 9; 16; 25]``

    Test passed.

+ 10 / 10: ``take 10 (map (fun x -> Float.round_up(x *. 100.0) /. 100.0 ) (sqrt_approximations 49.0))`` should evaluate to  ``[25.; 13.; 7.; 10.; 8.5; 7.75; 7.38; 7.19; 7.1; 7.05]``

    Test passed.

+ 10 / 10: ``take 10 (map (fun x -> Float.round_up(x *. 100.0) /. 100.0 ) (sqrt_approximations 48.0))`` should evaluate to  ``[24.5; 12.75; 6.88; 9.82; 8.35; 7.61; 7.25; 7.06; 6.97; 6.93]``

    Test passed.

+ 10 / 10: ``((Float.round_up (100.0 *. (epsilon_diff 1.0 (sqrt_approximations 50.0)))) /. 100.0)`` should evaluate to  ``6.36``

    Test passed.

+ 10 / 10: ``((Float.round_up (100.0 *. (epsilon_diff 0.1 (sqrt_approximations 50.0)))) /. 100.0)`` should evaluate to  ``7.03``

    Test passed.

+ 10 / 10: ``((Float.round_up (100.0 *. (epsilon_diff 0.01 (sqrt_approximations 50.0)))) /. 100.0)`` should evaluate to  ``7.08``

    Test passed.

+ 10 / 10: ``(Float.round_up(1000.0 *. sqrt_threshold 50.0 1.0) /. 1000.0)`` should evaluate to  ``7.125``

    Test passed.

+ 10 / 10: ``(Float.round_up(1000.0 *. sqrt_threshold 50.0 0.10) /. 1000.0)`` should evaluate to  ``7.078``

    Test passed.

+ 10 / 10: ``(Float.round_up(1000.0 *. sqrt_threshold 50.0 0.010) /. 1000.0)`` should evaluate to  ``7.072``

    Test passed.

### Total score

+ 120 / 120: total score for this assignment

