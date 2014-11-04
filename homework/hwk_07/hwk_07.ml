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
(*####################### TO REMOVE ########################*)
let show_list f l =
  let rec sl f l =
    match l with 
    | [] -> ""
    | [x] -> f x
    | x::xs -> f x ^ "; " ^ sl f xs
  in "[ " ^ sl f l ^ " ]"

let show_pair f (x,y) = "(" ^ f x ^ ", " ^ f y ^ ")"

let rec show_result = function
  | OK  -> "OK"
  | FileNotFound filename -> "FileNotFound " ^ filename
  | IncorrectNumLines n -> "IncorrectNumLines " ^ Int.to_string n
  | IncorrectLines xs -> "IncorrectLines " ^
               show_list (show_pair Int.to_string) xs
  | IncorrectLastStanza -> "IncorrectLastStanza"
(*############################################################*)
let is_elem (a:'a) (lst: 'a list):bool = 
  (filter (fun b -> b=a) lst) <> [] 

let split_by (eq:'a -> 'a -> bool) (ls: 'a list) (kill: 'a list) =
  let wrap ((lista: 'a list list), (listb: 'a list)) (e:'a) =
    if (filter (fun b -> (eq b e)) kill <> []) then (lista@[listb], []) else (lista, listb@[e])
  in let(l1,l2) = foldl wrap ([],[]) ls 
     in  filter (fun x -> x <> []) (l1@[l2]) (*parens needed or else filter only works on l1*)

let length (lst: 'a list):int = foldl (fun x _ -> x+1) 0 lst

type word = char list
type line = word list

let convert_to_non_blank_lines_of_words (poem:string):line list = 
  let line: word list = split_by (=) (String.to_list poem) ['\n']
  in
  let curr = fun x -> split_by (=) x [' ';'.';'!';'?';',';';';':';'-';',']
  in 
  filter (fun x -> x <> []) (map curr line)

let get_text (fn:string) : string option =
  try
    Some (In_channel.read_all fn)
  with 
  | _ -> None


type result = OK 
            | FileNotFound of string
            | IncorrectNumLines of int 
            | IncorrectLines of (int * int) list
            | IncorrectLastStanza

 
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





(*
##wrong is_elem method
let is_elemWrong (a:'a) (lst: 'a list) = (foldl (fun x -> x = a)false lst)
##Long is_elem but works! 
let is_elem (a:'a) (lst: 'a list):bool = 
  match (filter (fun b -> b=a) lst) with
  | [] -> false
  | _ -> true

##Log split_by

let split_by (eq:'a -> 'a -> bool) (ls: 'a list) (kill: 'a list) =
  let aux (a:'a) (lst: 'a list):bool = (filter (fun b -> (eq b a)) lst) <> []
  in
  let wrap ((lista: 'a list list), (listb: 'a list)) (e:'a) =
    if (aux e kill) then (lista@[listb], []) else (lista, listb@[e])
  in let(l1,l2) = foldl wrap ([],[]) ls 
     in  filter (fun x -> x <> []) l1@[l2]
 *)

(*map (( fun x -> map (fun x -> x+1) x )) [[1;2;3];[4;5;6];[8;9;10]] *)
