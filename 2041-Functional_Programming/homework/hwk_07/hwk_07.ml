(*#########@@@## HELPER FUNCTIONS ####################*)
let rec filter (f:'a -> bool) (l:'a list) : 'a list =
  match l with
  | [] -> []
  | x::xs -> let rest = filter f xs
	     in if f x then x :: rest else rest

let rec map (f:'a -> 'b) (l:'a list) : 'b list =
  match l with
  | [] -> []
  | x::xs -> f x :: map f xs

let rec foldr (f:'a -> 'b -> 'b) (v:'b) (l:'a list) : 'b =
  match l with
  | [] -> v
  | x::xs -> f x (foldr f v xs)

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

let is_elem (a:'a) (lst: 'a list):bool = (filter (fun b -> b=a) lst) <> [] 

let split_by (eq:'a -> 'a -> bool) (ls: 'a list) (kill: 'a list) =
  let wrap ((lista: 'a list list), (listb: 'a list)) (e:'a) =
    if (filter (fun b -> (eq b e)) kill <> []) then (lista@[listb], []) else (lista, listb@[e])
  in let(l1,l2) = foldl wrap ([],[]) ls 
     in  filter (fun x -> x <> []) (l1@[l2]) (*parens needed or else filter only works on l1*)

let length (lst: 'a list):int = foldl (fun x _ -> x+1) 0 lst

type word = char list
type line = word list

let convert_to_non_blank_lines_of_words (poem:string):line list = 
  let line: word list = split_by (=) (map Char.lowercase (String.to_list poem)) ['\n']
  in
  let curr = fun x -> split_by (=) x [' ';'.';'!';'?';',';';';':';'-';',']
  in 
  filter (fun x -> x <> []) (map curr line)

let get_text (fn:string) : string option =
  try
    Some (In_channel.read_all fn)
  with 
  | _ -> None
(*#######################END HELPER FUNCTIONS ###########################*)

type result = OK 
            | FileNotFound of string
            | IncorrectNumLines of int 
            | IncorrectLines of (int * int) list
            | IncorrectLastStanza

let paradelle (fileName:string):result = 
  let cmp = fun x y-> if x>y then 1 else if x=y then 0 else -1 in
  let validateLastStanza lastStanza first3 = 
    if List.sort cmp (List.dedup (List.concat lastStanza)) <> List.sort cmp (List.dedup (List.concat first3)) then IncorrectLastStanza else OK
  in 
  let stanzaCheck text (seed:int) = 
    match text with
      | a1::a2::a3::a4::a5::a6::[] ->
	 if a1 <> a2 then (if a3 <> a4 then [(seed,seed+1);(seed+2,seed+3)] else [(seed,seed+1)]) 
	 else if a3 <> a4 then [(seed+2,seed+3)]
	 else 
	   if List.sort (cmp) (a5@a6) <> List.sort (cmp) (a1@a3) then [(seed+4,seed+5)] else [(888,888)]
      | _ -> [(1000,1000)] (*should never get here*)
  in 
  let mainChecker (text:line list) =
    if length(text) <> 24 then IncorrectNumLines (length text)
    else 
      let first3 = (filter (fun x -> x <> (888,888)))   (  (stanzaCheck (take 6 text) 1)@ 
							 (stanzaCheck (drop 6 (take 12 text)) 7)@  
							 (stanzaCheck (drop 12 (take 18 text)) 13)) in
      match first3 with 
      | [] -> validateLastStanza (drop 18 text) (take 18 text)
      | _ -> IncorrectLines first3
  in  
  match get_text(fileName) with
  | None -> FileNotFound fileName 
  | Some x -> mainChecker (convert_to_non_blank_lines_of_words x)

assert ( paradelle "paradelle_susan_1.txt" = OK )
assert ( paradelle "paradelle_susan_2.txt" = OK )
assert ( paradelle "paradelle_emma_1.txt"  = OK )

assert ( paradelle "not_a_paradelle_susan_1.txt" <> OK )
assert ( paradelle "not_a_paradelle_susan_2.txt" <> OK )
assert ( paradelle "not_a_paradelle_emma_1.txt"  <> OK )

assert ( paradelle "not_a_paradelle_empty_file.txt"  <> OK )
assert ( paradelle "not_a_paradelle_wrong_line_count.txt"  <> OK )


assert ( paradelle "not_a_paradelle_susan_1.txt" = 
       IncorrectLines [(1, 2); (11, 12); (17, 18)] )

assert ( paradelle "not_a_paradelle_susan_2.txt" =
       IncorrectLines [(11, 12); (17, 18)] )

assert ( paradelle "not_a_paradelle_susan_3.txt" = 
       IncorrectLines [(1, 2); (11, 12); (17, 18)] )

assert ( paradelle "not_a_paradelle_emma_1.txt" = 
       IncorrectLastStanza )

assert ( paradelle "not_a_paradelle_empty_file.txt"  =
       IncorrectNumLines 0 ) 

assert ( paradelle "not_a_paradelle_wrong_line_count.txt" =
       IncorrectNumLines 9 )


(* Debug stuff *)
(*
let emma1 = show_result (paradelle "paradelle_emma_1.txt")
let notsusan1 = show_result (paradelle "not_a_paradelle_susan_1.txt")

let emmaRaw = convert_to_non_blank_lines_of_words (In_channel.read_all("paradelle_emma_1.txt"))
let examineRef = take 18 emmaRaw
let examineLast = drop 18 emmaRaw


(*######################## SUPPLIED ########################*)
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
(*################END OF SUPPLIED FUNCTIONS ###############*)

*)

(*
##wrong is_elem method
let is_elemWrong (a:'a) (lst: 'a list) = (foldl (fun x -> x = a)false lst)
##Long is_elem but works! 
let is_elem (a:'a) (lst: 'a list):bool = 
  match (filter (fun b -> b=a) lst) with
  | [] -> false
  | _ -> true

##Long split_by from hwk6, shorter is optimized

let split_by (eq:'a -> 'a -> bool) (ls: 'a list) (kill: 'a list) =
  let aux (a:'a) (lst: 'a list):bool = (filter (fun b -> (eq b a)) lst) <> []
  in
  let wrap ((lista: 'a list list), (listb: 'a list)) (e:'a) =
    if (aux e kill) then (lista@[listb], []) else (lista, listb@[e])
  in let(l1,l2) = foldl wrap ([],[]) ls 
     in  filter (fun x -> x <> []) l1@[l2]
 *)

(*map (( fun x -> map (fun x -> x+1) x )) [[1;2;3];[4;5;6];[8;9;10]] *)
