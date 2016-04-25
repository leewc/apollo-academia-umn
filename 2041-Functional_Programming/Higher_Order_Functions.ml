let rec map (f:'a -> 'b) (l:'a list) : 'b list =
  match l with
  | [] -> []
  | x::xs -> f x :: map f xs

let rec filter (f:'a -> bool) (l:'a list) : 'a list =
  match l with
  | [] -> []
  | x::xs -> let rest = filter f xs
	     in if f x then x :: rest else rest

let rec foldl f v l =
  match l with
  | [] -> v
  | x::xs ->  foldl f (f v x) xs

let rec foldr f v l = match l with
  | [] -> v
  | x::xs -> f x (foldr f v xs)


(*map using foldr *)
let foldr_map f l = foldr (fun x xs -> (f x) :: xs ) [] l 

(*map using foldl*)
let foldl_map f l = foldl (fun x xs -> x @ [(f xs)]) [] l

(*filter using foldr*)
let foldr_filter f l = foldr (fun x xs -> if (f x) then x :: xs else xs ) [] l

(*filter using foldl*)
let foldl_filter f l = foldl ( fun x xs -> if (f xs) then x @ [xs] else x) [] l
