type expr 
  = Const of int
  | Add of  expr * expr
  | Mul of expr * expr
  | Sub of expr * expr
  | Div of expr * expr
  | Let of string * expr * expr
  | Var of string


(* Place functions show_expr and show_pretty_expr in this file. *)

let show_pretty_expr (exp:expr): string = 
   let rec pp ex prec left
    (* can pass down the previous expression to determine if we need
       also need to check which child it is to determine if we need parens or not
       like for the case of 1-2-3 and 1-(2-3), which are different
       left is a boolean
     *)
