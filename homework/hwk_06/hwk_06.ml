(*----------Helper Functions -------------*)
let rec filter (f:'a -> bool) (l:'a list) : 'a list =
  match l with
  | [] -> []
  | x::xs -> let rest = filter f xs
	     in if f x then x :: rest else rest

let rec map (f:'a -> 'b) (l:'a list) : 'b list =
  match l with
  | [] -> []
  | x::xs -> f x :: map f xs

(* fold (+) 0 [1;2;3;4] as 1 + (2 + (3 + (4 + 0)))*)
let rec foldr (f:'a -> 'b -> 'b) (v:'b) (l:'a list) : 'b =
  match l with
  | [] -> v
  | x::xs -> f x (foldr f v xs)

(* fold (+) 0 [1;2;3;4] as((((0 + 1) + 2) + 3) + 4) *)
let rec foldl f v l =
  match l with
  | [] -> v
  | x::xs ->  foldl f (f v x) xs

let rec take (n:int) (lst:'a list): 'a list  =
  match lst with
  | [] -> [] 
  | x::xs -> if n=0 then [] else x::(take (n-1) xs)

let rec drop (n:int) (lst:'a list): 'a list =
  match lst with
  | [] -> []
  | x::xs -> if n=0 then x::xs else drop (n-1) xs
(*-------End: Helper Functions---------------------*)

let is_elem (a:'a) (lst: 'a list):bool = 
  match (filter (fun b -> if b=a then true else false) lst) with
  | [] -> false
  | _ -> true

(*split_by evaluates elements from ls with the kill list using the equality function, where aux is a helper function that does thi, and wrapper contructs the output list*)
let split_by (eq:'a -> 'a -> bool) (ls: 'a list) (kill: 'a list) =
  let aux (a:'a) (lst: 'a list):bool =
  match (filter (fun b -> if (eq b a) then true else false) lst) with
  | [] -> false
  | _ -> true
  in
  let wrap ((lista: 'a list list), (listb: 'a list)) (e:'a) =
    match (aux e kill) with
    | true -> (lista@[listb], [])
    | false -> (lista, listb@[e])
  in let(l1,l2) = foldl wrap ([],[]) ls 
     in match l2 with 
	| [] -> filter (fun x -> not (x = [])) l1
	| _ ->  filter (fun x -> not (x = [])) l1@[l2]
(*the last l1@[l2] appends any leftover items in the list*)
(*filter required to remove [] generated when there is , and space*)


let length (lst: 'a list):int =
  match lst with 
  | [] -> 0 (*prevent not exhaustiveness*)
  | _ -> let count a lst= a+1 in foldl count 0 lst


type word = char list
type line = word list

let convert_to_non_blank_lines_of_words (poem:string):line list = 
  let line: word list = split_by (=) (String.to_list poem) ['\n']
  in
  let curr = fun x -> split_by (=) x [' ';'.';'!';'?';',';';';':';'-';',']
  in 
  filter (fun x -> not (x = [])) (map curr line)
(*filter was to get rid of double newlines*)

let get_text (fn:string) : string option =
  try
      Some (In_channel.read_all fn)
  with 
  | _ -> None



assert (is_elem 4 [1;2;3;4;5;6])
assert (not (is_elem 7 [1;2;3;4;5;6;8;9;10] ) )
assert (is_elem "Hello" ["Why"; "not";  "say"; "Hello"])
assert (not (is_elem 3.5 [ ]) )


assert ( split_by (=) [1;2;3;4;5;6;7;8;9;10;11] [3;7] =
         [ [1;2]; [4;5;6]; [8;9;10;11] ] )
assert ( split_by (=) ["A"; "B"; "C"; "D"] [] =
         [["A"; "B"; "C"; "D"]] )


assert ( length [] = 0 )
assert ( length [1;2;3;4] = 4 )
assert ( length ["Hello"] = 1 )


assert ( let text = In_channel.read_all "paradelle_susan_1.txt"
         in length (convert_to_non_blank_lines_of_words text) = 24 )

assert ( let text = In_channel.read_all "paradelle_susan_2.txt"
         in length (convert_to_non_blank_lines_of_words text) = 24 )

assert ( let text = In_channel.read_all "paradelle_emma_1.txt"
         in length (convert_to_non_blank_lines_of_words text) = 24 )

assert ( let text = In_channel.read_all "not_a_paradelle_susan_1.txt"
         in length (convert_to_non_blank_lines_of_words text) = 24 )

assert ( let text = In_channel.read_all "not_a_paradelle_susan_2.txt"
         in length (convert_to_non_blank_lines_of_words text) = 24 )

assert ( let text = In_channel.read_all "not_a_paradelle_emma_1.txt"
         in length (convert_to_non_blank_lines_of_words text) = 24 )

assert ( let text = In_channel.read_all "not_a_paradelle_empty_file.txt"
         in length (convert_to_non_blank_lines_of_words text) = 0 )

assert ( let text = In_channel.read_all "not_a_paradelle_wrong_line_count.txt"
         in length (convert_to_non_blank_lines_of_words text) = 9 )

assert ( let text = In_channel.read_all "paradelle_susan_1.txt"
     in  match convert_to_non_blank_lines_of_words text with
         | line1::rest -> length line1 = 9
         | _ -> false ) 
 



(*fails --ignore*)
(*
let split_by (z:'a -> 'a -> bool) (input: 'a list) (kill: 'a list) =
  let is = (fun x -> is_elem x kill) (*takes input list outputs true/false if elem is in kill list, to swap with loaded func*)
  in 
  let compose z y = (match z with (*if z is false then put corresponding y in there, where z,y are elements*)
    | true -> y
    | false -> y)
  in let cur = (fun x -> compose(is x) x)
  in map cur input 
  (*map curry input*)


let convert_to_non_blank_lines_of_words (poem:string):line list = 
  let chrls = String.to_list poem
  in
  let lines:word list = split_by (=) chrls [' ';',';'.';'!'] 
  (*splits into words*)
  in split_by (=) (lines) [['\n']]
 *)
