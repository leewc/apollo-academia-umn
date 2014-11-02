Below are the results of the initial grading for homework 6.

An additional manual inspection of your code is also being carried out.  The results of that analysis will be put into another file that will be committed to this same directory in your repository.

The TAs will shortly double check the cases in which a very low score was reported. Thus, if your score is very low and you feel you at least nearly completed the work, please wait for this manual check to be completed.

After this manual process has finished, these lines will be removed and the word "initial" from the first line will be removed. If at that point, there is a grading concern that needs addressing please email **csci2041@cs.umn.edu** with your question or request.  Be sure to address that email to the TA that is your "contact person" so that they can address your concerns.  If you are unsure who this is, please see the "Contact Person" page linked to in the top section of the course Moodle page.

## Scores from homework hwk_06.ml.

+ 3 / 3: Functions are put into the appropriate file: ``homework/hwk_06/hwk_06.ml``

    File stored correctly in ``homework/hwk_06/hwk_06.ml``.



+ 15 / 15: File should have no errors or failing assertions.

    Test passed.

+ 3 / 3: ``is_elem 4 [1;2;3;4;5;6]`` should evaluate to ``true``

    Test passed.

+ 2 / 2: ``is_elem 6 [1;2;3;4;5;7;8;9;10]`` should evaluate to ``false``

    Test passed.

+ 2 / 2: ``is_elem "Hello" ["Why"; "not"; "say"; "Hello"]`` should evaluate to ``true``

    Test passed.

+ 2 / 2: ``is_elem "Hi" ["Why"; "not"; "say"; "Hello"]`` should evaluate to ``false``

    Test passed.

+ 2 / 2: ``is_elem 12.5 [ ]`` should evaluate to ``false``

    Test passed.

+ 2 / 2: ``length []``

    Test passed.

+ 3 / 3: ``length [1;2;3;4]``

    Test passed.

+ 3 / 3: ``length [1;3;4]``

    Test passed.

+ 3 / 3: ``length ["Hello"; "World"]``

    Test passed.

+ 5 / 5: ``split_by (=) [1;2;3;4;5;6;7;8;9;10;11] [3;7]`` should evaluate to ``[ [1;2]; [4;5;6]; [8;9;10;11] ]``

    Test passed.

+ 5 / 5: ``split_by (=) [10;20;30;40;50;60;70;80;90;100;110] [20;60]`` should evaluate to ``[ [10]; [30;40;50]; [70;80;90;100;110] ]``

    Test passed.

+ 5 / 5: ``split_by (=) ["A"; "B"; "C"; "D"] []`` should evaluate to ``[["A"; "B"; "C"; "D"]]``

    Test passed.

+ 5 / 5: ``split_by (=) ["zA"; "zB"; "zC"; "zD"] []`` should evaluate to ``[["zA"; "zB"; "zC"; "zD"]]``

    Test passed.

+ 5 / 5: ``split_by (fun _ x -> x mod 2 = 0) [1;3;5;2;7;9;4;11] [0]`` should evaluate to ``[[1; 3; 5]; [7; 9]; [11]]``

    Test passed.

+ 5 / 5: ``split_by (fun sep x -> sep + 2 = x) [1;3;5;2;7;9;4;11] [1;5]`` should evaluate to ``[ [1]; [5;2]; [9;4;11] ]``

    Test passed.

+ 5 / 5: ``let text = In_channel.read_all "paradelle_susan_1.txt"  in List.length (convert_to_non_blank_lines_of_words text)`` should evaluate to ``24``

    Test passed.

+ 5 / 5: ``let text = In_channel.read_all "test_file_1.txt"  in List.length (convert_to_non_blank_lines_of_words text)`` should evaluate to ``24``

    Test passed.

+ 5 / 5: ``let text = In_channel.read_all "not_a_paradelle_wrong_line_count.txt"  in List.length (convert_to_non_blank_lines_of_words text)`` should evaluate to ``9``

    Test passed.

+ 5 / 5: ``let text = In_channel.read_all "test_file_2.txt"  in List.length (convert_to_non_blank_lines_of_words text)`` should evaluate to ``9``

    Test passed.

+ 5 / 5: ``let text = In_channel.read_all "not_a_paradelle_empty_file.txt"  in List.length (convert_to_non_blank_lines_of_words text)`` should evaluate to ``0``

    Test passed.

+ 5 / 5: ``let text = In_channel.read_all "test_file_3.txt"  in List.length (convert_to_non_blank_lines_of_words text)`` should evaluate to ``0``

    Test passed.

### Total score

+ 100 / 100: total score for this assignment

