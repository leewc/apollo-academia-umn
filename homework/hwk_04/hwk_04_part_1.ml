type expr 
  = Const of int
  | Add of  expr * expr
  | Mul of expr * expr
  | Sub of expr * expr
  | Div of expr * expr
  | Let of string * expr * expr
  | Var of string


(* Place functions show_expr and show_pretty_expr in this file. *)

let show_expr (b:expr):string = 
  let rec s_ex (a:expr) (out:string):string = 
    match a with 
    | Const n -> out^(string_of_int n)
    | Add (l,r) -> "("^(s_ex l out)^"+"^(s_ex r out)^")"
    | Mul (l,r) -> "("^(s_ex l out)^"*"^(s_ex r out )^")"
    | Sub (l,r) -> "("^(s_ex l out)^"-"^(s_ex r out)^")"
    | Div (l,r) -> "("^(s_ex l out)^"/"^(s_ex r out)^")"
    | Let (s,l,r) -> "(let "^s^"="^(s_ex l out)^" in "^(s_ex r out)^")"
    | Var a -> out^a
  in s_ex b ""

(*
let show_pretty_expr (exp:expr): string = 
   let rec pp ex prev left
     can pass down the previous expression to determine if we need
       also need to check which child it is to determine if we need parens or not
       like for the case of 1-2-3 and 1-(2-3), which are different
       left args is a boolean

       maybe have a type whichchild = LeftChild | RightChild

145 ===> 160
200+ for furniture
     *)

(* a:input expression r:bool if on right side and p:previous expr*)
let show_pretty_expr (exp:expr):string  =
  let isLast (a:expr) (b:expr):bool = 
    match a with
    | Add (l,r) -> if (compare r b = 0) then true else false
  in 
  let rec pexp (azz:expr) (r:bool):string = 
    match (azz,r) with
    | (Const n, _) -> (string_of_int n)
    | (Add (l,r), true) -> "("^(pexp l false)^"+"^(pexp r true)^")"
    | (Add (l,r), false) -> (pexp l false)^ "+"^(pexp r true)
    | (Mul (l,r), true) -> (pexp l false)^"*"^(pexp r true)
    | (Mul (l,r), false) -> (pexp l false)^"*"^(pexp r true)
    | (Sub (l,r), true) -> "("^(pexp l false)^"-"^(pexp r true)^")"
    | (Sub (l,r), false) -> (pexp l false)^"-"^(pexp r true)
    | (Div (l,r), true) -> "("^(pexp l false)^"/"^(pexp r true)^")"
    | (Div (l,r), false) -> (pexp l false)^"/"^(pexp r true)
    | (Var a ,_ )-> a
    | (Let (s,l,r), r2) -> (match ((s,l,r),r2,exp) with 
			| ((s,l,r), false, Let _) -> "c1 let "^s^"="^(pexp l false)^" in "^(pexp r false)
			| ((s,l,r), false, _) -> "(c2 let "^s^"="^(pexp l false)^" in "^(pexp r true) ^")"
			| ((s,l,r4), true, Add _) -> if(isLast exp r4) then "c4a let "^s^"="^(pexp l false)^" in "^(pexp r false)
						    else "(c4 let "^s^"="^(pexp l false)^" in "^(pexp r false)^")"
			| ((s,l,r), true, _) -> "c3 let "^s^"="^(pexp l false)^" in "^(pexp r true)
		    )  
    
  in pexp exp false 

