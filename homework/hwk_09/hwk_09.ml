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
  Function takes in a list of strings (from freevars) and returns all possible subst combinations, 
this is split from is_tautology as a design choice in an attempt to simplify code.
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


(*
let is_tautology (f:formula) (funSubst: subst -> subst option): subst option= 
  let vars = freevars f in   (*generates list of vars. 'string list*)
  let rec gen_subst (sub:subst) (varList:'subst list): subst =
    match varList with
    | [] -> subst
    | x::xs -> if (is_elem sub varList) then gen_subst 
 *)






assert (eval (And ( Prop "P", Prop "Q")) [("P",true); ("Q",false)] = false )
assert (eval (And ( Prop "P", Prop "Q")) [("P",true); ("Q",true)] = true )
assert ( (freevars (And ( Prop "P", Prop "Q")) = ["P"; "Q"]) || (freevars (And ( Prop "P", Prop "Q")) = ["Q"; "P"]) )
assert ( List.length (freevars (And ( Prop "P", Or (Prop "Q", Prop "P")))) = 2)




(*Code Fails*)

(*
    else [(true :: (tf (n-1)))] @ (false :: (tf (n-1)))]
  in tf (List.length vars)
*)

(*let left = [table_make xs (out@[(x,true)]) ] in 
	       left @ [(table_make xs (out@[(x,false)]))] 
  in table_make vars [] *)
