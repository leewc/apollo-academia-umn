let rec take (n:int) (lst:'a list): 'a list  =
  match lst with
  | [] -> [] 
  | x::xs -> if n=0 then [] else x::(take (n-1) xs)

let rec drop (n:int) (lst:'a list): 'a list =
  match lst with
  | [] -> []
  | x::xs -> if n=0 then x::xs else drop (n-1) xs

let rec take_while (f:'a -> bool) (lst:'a list): 'a list =
  match lst with
  | [] -> []
  | x::xs -> if (f x) then x::(take_while f xs) else (take_while f xs)

type estring = char list

let rec map (f:'a -> 'b) (l:'a list) : 'b list =
  match l with
  | [] -> []
  | x::xs -> f x :: map f xs

let string_to_estring s = String.to_list s

let estring_to_string es = String.concat (map Char.to_string es)

let capitalize (es:estring): estring =
  map (fun ch -> match ch with 
		 | x -> Char.uppercase x) es
