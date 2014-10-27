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


let split_by (z:'a -> 'a -> bool) (input: 'a list) (kill: 'a list) =
  let is = (fun x -> is_elem x kill) (*takes input list outputs true/false if elem is in kill list, to swap with loaded func*)
  in 
  let compose z y hold= (match z with (*if z is false then put corresponding y in there, where z,y are elements*)
    | true -> hold
    | false -> hold@y)
  in let cur = (fun x -> compose(is x) x [])
  in map cur input 
  (*map curry input*)

let length (lst: 'a list):int =
  match lst with 
  | [] -> 0
  | _ -> let count a lst= a+1 in foldl count 0 lst

type word = char list
type line = word list
(*
let convert_to_non_blank_lines_of_words (poem:string) = 
  let lineb p = filter (fun a -> match a with | "\n" -> false | _ -> true) p 
  in lineb poem
 *)


let get_text (fn:string) : string option =
  try
      Some (In_channel.read_all fn)
  with 
  | _ -> None
