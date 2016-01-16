type expr 
  = Const of int
  | Add of  expr * expr
  | Mul of expr * expr
  | Sub of expr * expr
  | Div of expr * expr
  | Let of string * expr * expr
  | Var of string

(*
const 0 var 0 - but don't care
add, sub 1
mul, div 2
let has highest
wrapper function to wrap it. 
 *)

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

(*improved version*)
let show_pretty_expr (a:expr):string = 
  let parens n = "(" ^ n ^ ")" in
  let pcd d = 
    match d with
    | Const a -> 0 
    | Var a -> 0
    | Add (a,b) -> 1  
    | Sub (a,b) -> 1
    | Mul (a,b) -> 2  
    | Div (a,b) -> 2
    | Let (a,b,c) -> 3
  in 
  let rec s_ex (a:expr) (pp:int) (blockedAtRight:bool) (shouldWrap:bool) (out:string):string =
    match a with
    | Const n -> out^(string_of_int n)
    | Add (l,r) -> if (pcd a < pp || not blockedAtRight || shouldWrap) then (s_ex l (pcd a) false false out)^"+"^(s_ex r (pcd a) true false out)  
		   else  parens ((s_ex l (pcd a) false false out)^"+"^ (s_ex r (pcd a) true false out))

    | Sub (l,r) ->  if (pcd a < pp || not blockedAtRight || shouldWrap) then (s_ex l (pcd a) false false out)^"-"^(s_ex r (pcd a) true false out)  
		   else  parens ((s_ex l (pcd a) false false out)^"-"^ (s_ex r (pcd a) true false out))

    | Mul (l,r) -> if (pcd a < pp && pcd a > 0 || not blockedAtRight || shouldWrap) then (s_ex l (pcd a) false false out)^"*"^parens((s_ex r (pcd a) true false out))  
		   else  parens ((s_ex l (pcd a) false false out)^"*"^ (s_ex r (pcd a) true false out))

    | Div (l,r) -> if (pcd a < pp || not blockedAtRight || shouldWrap) then (s_ex l (pcd a) false false out)^"/"^parens(s_ex r (pcd a) true false out)  
		   else  parens ((s_ex l (pcd a) false false out)^"/"^ (s_ex r (pcd a) true false out))

    | Let (s,l,r) -> if (pcd a < pp || blockedAtRight || shouldWrap) then ( "let "^s^"="^(s_ex l (pcd a) true false out)^" in "^(s_ex r (pcd a) true false out) )
		     else if (pcd a = pp || blockedAtRight || shouldWrap) then  parens( ("let "^s^"="^(s_ex l (pcd a) false false out)^" in "^ ((s_ex r (pcd a) true false out) )))
		     else "let "^s^"="^(s_ex l (pcd a) false false out) ^ " in "^ (s_ex r (pcd a) true false out)
    | Var a -> out^a
  in s_ex a 1 false false ""

let show_pretty_expr (e:expr):string =
  let prec = function
    | Let _ -> 1
    | Add _ | Sub _ -> 2
    | Mul _ | Div _ -> 3
    | Const _ | Var _ -> 4
  in let opsym = function
       | Add _ -> "+"
       | Sub _ -> "-"
       | Mul _ -> "*"
       | Div _ -> "/"
     in let wrap doso str =
if doso then "(" ^ ex ^ ")" else str in
	let islet = function
	  | Let _ -> true
	  | _ -> false
in
  let rec helper (ex:expr) (blockedatright:bool) =
    match ex with
    | Add (l,r) | Sub (l,r) | Mul (l,r) | Div (l,r) -> wrap (prec ex > prec l || islet l) (helper l false) ^ opsym ex ^ let shouldwrap = prec ex >= prec l || islet r && not blockedatright in wrap shouldwrap (helper r (blockedatright||shouldwrap))
    | Let (a,b,c) -> "Let "^a^" in" ^ helper l false ^ helper r true 
  in helper e true
(*
higher lower left
same left *)







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


(*
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

 *)
