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

+ 5 / 5: ``split_by (fun x y -> if x = 0 then y mod 2 = 0 else x mod 2 = 0) [1;3;5;2;7;9;4;11] [0]`` should evaluate to ``[[1; 3; 5]; [7; 9]; [11]]``

    Test passed.

+ 5 / 5: ``split_by (fun x sep -> abs(sep - x) = 2) [1;3;5;2;7;9;4;11] [1;5]`` should evaluate to ``[ [1]; [5;2]; [9;4;11] ]``

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

+ 10 / 10: ``let text = In_channel.read_all "test_file_4.txt"  in List.length (convert_to_non_blank_lines_of_words text)`` should evaluate to ``9``

    Test passed.

### Total score

+ 110 / 100: total score for this assignment

