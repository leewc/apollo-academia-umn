type expr 
  = Const of int
  | Add of  expr * expr
  | Mul of expr * expr
  | Sub of expr * expr
  | Div of expr * expr
  | Let of string * expr * expr
  | Var of string


(* Place functions show_expr and show_pretty_expr in this file. *)
