type formula = And of formula * formula
             | Or  of formula * formula
             | Not of formula 
             | Prop of string
             | True
             | False

exception KeepLooking

type subst = (string * bool) list

(*################## Helper Functions ####################*)
let show_list show l =
  let rec sl l =
    match l with 
    | [] -> ""
    | [x] -> show x
    | x::xs -> show x ^ "; " ^ sl xs
  in "[ " ^ sl l ^ " ]"

let show_string_bool_pair (s,b) =
  "(\"" ^ s ^ "\"," ^ (if b then "true" else "false") ^ ")"

let show_subst = show_list show_string_bool_pair

let rec foldr f v l = match l with
  | [] -> v
  | x::xs -> f x (foldr f v xs)

let is_elem v l =
  foldr (fun x in_rest -> if x = v then true else in_rest) false l

let rec map (f:'a -> 'b) (l:'a list) : 'b list =
  match l with
  | [] -> []
  | x::xs -> f x :: map f xs

let rec filter (f:'a -> bool) (l:'a list) : 'a list =
  match l with
  | [] -> []
  | x::xs -> let rest = filter f xs
	     in if f x then x :: rest else rest

let rec is_not_elem set v =
  match set with
  | [] -> true
  | s::ss -> if s = v then false else is_not_elem ss v

(*########################  Written Code  ################################ *)

(*formula -> subst -> bool*)
let rec eval (f:formula) (s:subst) : bool =
  let in_subst (v:string) (l:subst) = 
    match (foldr (fun (x,y) in_rest-> if x = v then in_rest@[y] else in_rest) [] l) with 
    | [x] -> x
    | _ -> raise (Failure("Prop not found"))
  in 
  match f with 
  | Or (x,y) -> (eval x s) || (eval y s) 
  | And (x,y) -> (eval x s) && (eval y s)
 (* | Not (Prop x) -> not (in_subst x s)  this is redundant*)
  | Not x -> not (eval x s)
  | Prop p -> in_subst p s 
  | True -> true
  | False -> false

let freevars (f:formula):string list =
  let rec helper f l = 
    match f with 
    | Or (x,y)
    | And (x,y) -> (helper x l) @ (helper y l) 
    | Not x -> helper x l
    | Prop p -> l@[p]  
    | True
    | False -> l
  in List.dedup (helper f [])

(*
  Function takes in a list of strings (from freevars) and returns all possible 
  subst combinations, this is split from is_tautology as a design choice in an 
  attempt to simplify code.
         string list -> subst list
*)
let subst_gen vars : subst list =
  let rec t n =  (*generates all true false combination, help from TA*)
    if n = 1 then [[true];[false]] 
    else (map (fun x ->  true :: x) (t (n-1))) @ (map (fun x -> false :: x) (t (n-1)))  (*or do List.cons true,[] *)
  in 
  let rec zip listA listB =
    match (listA, listB) with
    | (x::xs,y::ys) -> (x,y) :: zip xs ys
    |  _ -> []
  in 
  let rec wrap bools =
    match bools with 
    | [] -> []
    | x::xs -> (zip vars x) :: wrap xs
  in wrap (t (List.length vars))

let is_tautology (f:formula) (funSubst: subst -> subst option): subst option= 
  let vars = subst_gen (freevars f) in   (*generates list of true/false subst list.*)
  let rec helper vars = 
    match vars with 
    | [] -> None
    | x::xs -> if not (eval f x) then (try (funSubst x) with
				       | KeepLooking -> helper xs)
	       else helper xs
  in helper vars  

(* Helper function that maps all possible moves. 
   Taken out of the maze function to evaluate it and reduce 
   length of code in Maze () since this serves as a mapping only
*)
let maze_moves xy = 
  match xy with 
  | (1,1) -> [(2,1)]
  | (2,1) -> [(3,1);(1,1)]
  | (3,1) -> [(3,2);(2,1)]
  | (4,1) -> [(4,2)]
  | (5,1) -> [(5,2)]
  | (1,2) -> [(2,2);(1,3)]
  | (2,2) -> [(3,2);(1,2)]  
  | (3,2) -> [(2,2);(4,2)]
  | (4,2) -> [(3,2);(4,1)]
  | (5,2) -> [(5,1);(5,3)]
  | (1,3) -> [(1,4);(1,2);(2,3)]
  | (2,3) -> [(1,3)]
  | (3,3) -> [(3,2);(4,3);(3,4)]
  | (4,3) -> [(3,3);(5,3)]
  | (5,3) -> [(5,2);(5,4)]
  | (1,4) -> [(1,3);(1,5)]
  | (2,4) -> [(2,5);(3,4)]
  | (3,4) -> [(3,3);(2,4);(4,4)]
  | (4,4) -> [(3,4);(4,5)]
  | (5,4) -> [(5,3)]
  | (1,5) -> [(1,4);(2,5)]
  | (2,5) -> [(2,4);(1,5)]
  | (3,5) -> [(4,5)]
  | (4,5) -> [(3,5);(5,5)]
  | (5,5) -> [(4,5)]

let maze () = 
  let rec go_from state path = 
    if state = (5,1) || state = (3,5) then path    (*Found goal, G, return the path found*)
    else 
      match filter (is_not_elem path) (maze_moves state) with 
      | [] -> raise KeepLooking
      | [a] -> go_from a (path@[a])
      | [a;b] -> (try go_from a (path@[a]) with 
		  | KeepLooking -> go_from b (path@[b]) )
      | [a;b;c] -> (try go_from a (path@[a]) with 
		    | KeepLooking -> try go_from b (path@[b]) with 
				     | KeepLooking -> go_from c (path@[c]) )
      | _ -> raise (Failure ("This shouldn't happen!"))
  in go_from (2,3) [(2,3)]
(*argument passed into go_from is the starting point, S*)




assert (eval (And ( Prop "P", Prop "Q")) [("P",true); ("Q",false)] = false )
assert (eval (And ( Prop "P", Prop "Q")) [("P",true); ("Q",true)] = true )
assert ( (freevars (And ( Prop "P", Prop "Q")) = ["P"; "Q"]) || (freevars (And ( Prop "P", Prop "Q")) = ["Q"; "P"]) )
assert ( List.length (freevars (And ( Prop "P", Or (Prop "Q", Prop "P")))) = 2)

(* Testing *)
let is_tautology_first f = is_tautology f (fun s -> Some s)

let is_tautology_print_all f =
  is_tautology 
    f
    (fun s -> print_endline (show_subst s); 
          raise KeepLooking)




(*Code Fails -- I left my ugly code here for reference, clean and lean code vs bad messy code*)

(*
    else [(true :: (tf (n-1)))] @ (false :: (tf (n-1)))]
  in tf (List.length vars)
*)

(*let left = [table_make xs (out@[(x,true)]) ] in 
	       left @ [(table_make xs (out@[(x,false)]))] 
  in table_make vars [] *)

(*

let maze_moves (x,y: int*int) : ((int * int) list)  = 
  let walls = [((1,1),(1,2));((2,1),(2,2));((2,2),(2,3));((2,3),(3,3));
	       ((2,3),(2,4));((2,4),(1,4));((2,5),(3,5));((3,5),(3,4));
	       ((3,1),(4,1));((4,2),(4,3));((4,3),(4,4));((4,1),(5,1));
	       ((4,2),(5,2));((4,4),(5,4));((5,4),(5,5));
	       (*maze borders below*)
	       ((1,1),(0,1));((1,1),(1,0));((1,2),(0,2));((1,3),(0,3));
	       ((1,4),(0,4));((1,5),(0,5));((1,5),(1,6));((2,5),(2,6));
	       ((3,5),(3,6));((4,5),(4,6));((5,5),(5,6));((5,5),(6,5));
	       ((5,4),(6,4));((5,3),(6,3));((5,2),(6,2));((5,1),(6,1));
	       ((5,1),(5,0));((4,1),(4,0));((3,1),(3,0));((2,1),(2,0));((2,1),(1,0));
	       (*deadends below*)
	       ((3,1),(3,2)); ((5,3),(5,4));((4,5),(5,5))]
  in 
  let move_allow (x1,y1) (x2,y2) = not (((is_elem ((x1,y1),(x2,y2)) walls) || (is_elem ((x2,y2),(x1,y1)) walls)))
  in 
  let rec m_list (x,y) prevxy path = 
    if (x,y) = (5,1) || (x,y) = (3,5) then (path@[(x,y)])    (*if we reach G*)
    else if (move_allow (x,y) (x-1,y) && not ((x-1,y) =prevxy)) then m_list (x-1,y) (x,y) (path@[(x,y)]) (*up*)
    else if (move_allow (x,y) (x,y+1) && not ((x,y+1) =prevxy)) then m_list (x,y+1) (x,y) (path@[(x,y)]) (*right*)
    else if (move_allow (x,y) (x+1,y) && not ((x+1,y) =prevxy)) then m_list (x+1,y) (x,y) (path@[(x,y)]) (*down*)
    else if (move_allow (x,y) (x,y-1) && not ((x,y-1) =prevxy)) then m_list (x,y-1) (x,y) (path@[(x,y)]) (*left*)
    else path@[(99,99)]
  in m_list (x,y) (100,100) [] (*100 as sentinel val, whole thing doesn't work since it's always up right down left*)


*)
