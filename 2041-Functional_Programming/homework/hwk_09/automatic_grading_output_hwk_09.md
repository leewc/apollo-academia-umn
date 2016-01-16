## Scores from homework hwk_09.ml.

+ 2 / 2: ``eval (And ( Prop "P", Prop "Q")) [("P",true); ("Q",false)]`` should evaluate to  ``false``

    Test passed.

+ 2 / 2: ``eval (And ( Prop "P", Prop "Q")) [("P",true); ("Q",true)]`` should evaluate to ``true``

    Test passed.

+ 3 / 3: ``eval (Or (Prop "P", Or (Prop "Q", Prop "R"))) [("P",false); ("Q",false); ("R",false)]`` should evaluate to ``false``

    Test passed.

+ 3 / 3: ``eval (Or (Prop "P", Or (Prop "Q", Prop "R"))) [("P",false); ("Q",false); ("R",true)]`` should evaluate to ``true``

    Test passed.

+ 3 / 3: ``eval (Or (Prop "P", Or (Prop "Q", Not (Prop "R")))) [("P",false); ("Q",false); ("R",true)]`` should evaluate to ``false``

    Test passed.

+ 3 / 3: ``eval (Or (Prop "P", Or (Prop "Q", Not (Prop "R")))) [("P",false); ("Q",false); ("R",false)]`` should evaluate to ``true``

    Test passed.

+ 5 / 5: ``(freevars (And ( Prop "P", Prop "Q")) = ["P"; "Q"]) || (freevars (And ( Prop "P", Prop "Q")) = ["Q"; "P"])`` should evaluate to ``true``

    Test passed.

+ 5 / 5: ``List.length (freevars (And ( Prop "P", Or (Prop "Q", Prop "P")))) = 2`` should evaluate to ``true``

    Test passed.

+ 5 / 5: ``freevars (And (True, False)) = [ ]`` should evaluate to ``true``

    Test passed.

+ 7 / 7: ``is_tautology_first (Or (Prop "P", Not (Prop "P"))) = None`` should evaluate to ``true`

    Test passed.

+ 7 / 7: ``is_tautology_first (Or (Or ( Not (Prop "P"), Prop "Q"), Or ( Not (Prop "Q"), Prop "P"))) = None`` should evaluate to ``true`

    Test passed.

+ 7 / 7: ``is_tautology_first (Or (Prop "P", Prop "Q")) <> None`` should evaluate to ``true`

    Test passed.

+ 7 / 7: ``is_tautology_first (Or (Prop "P", Prop "Q")) = Some [ ("Q", false); ("P", false) ] || is_tautology_first (Or (Prop "P", Prop "Q")) = Some [ ("P", false); ("Q", false) ]`` should evaluate to ``true``

    Test passed.

+ 7 / 7: ``let _ = results := [] in let _ = is_tautology_save_all (And (Prop "P", Prop "Q")) in List.length (!results) = 3`` should evaluate to ``true``

    Test passed.

+ 12 / 12: ``maze () <> None`` should evaluate to ``true``

    Test passed.

+ 12 / 12: `` maze () = Some [ (2,3); (1,3); (1,2); (2,2); (3,2); (3,3); (3,4); (4,4); (4,5); (3,5) ] || maze () = Some [ (2,3); (1,3); (1,2); (2,2); (3,2); (3,3); (4,3); (5,3); (5,2); (5,1) ] || maze () = Some [ (2,3); (1,3); (1,4); (1,5); (2,5); (2,4); (3,4); (3,3); (4,3); (5,3); (5,2); (5,1) ] || maze () = Some [ (2,3); (1,3); (1,4); (1,5); (2,5); (2,4); (3,4); (4,4); (4,5); (3,5) ]`` should evaluate to ``true``

    Test passed.

### Total score

+ 90 / 90: total score for this assignment

