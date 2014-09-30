type expr 
  = Add of  expr * expr
  | Mul of expr * expr
  | Sub of expr * expr
  | Div of expr * expr
  | Let of string * expr * expr
  | Var of string
  | LT of expr * expr
  | EQ of expr * expr
  | And of expr * expr
  | Not of expr
  | IfThenElse of expr * expr * expr
  | IntConst of int
  | BoolConst of bool


type value = IntVal of int | BoolVal of bool


let eval (e:expr) : value =
  let rec lookup n env = 
    match env with 
    | [ ] -> raise (Failure ("Identifier \"" ^ n ^ "\" not declared."))
    | (name,value)::rest -> if n = name then value else lookup n rest
  in
  let rec eval_h e env = match e with
    | Add (l,r) -> 
        let v1 = eval_h l env  and  v2 = eval_h r env
        in (match v1,v2 with 
            | IntVal x, IntVal y -> IntVal (x + y)
            | _ -> raise (Failure "Addition requires 2 integer values."))

    | IntConst v -> IntVal v
    | BoolConst b -> BoolVal b

    (* Many cases missing here, you need to complete them. *)

  in eval_h e []



type int_expr =
  | Add_int of int_expr * int_expr
  | Mul_int of int_expr * int_expr
  | Sub_int of int_expr * int_expr
  | Div_int of int_expr * int_expr
  | IntConst_int of int
  | Var_int of string
  | Let_int_int of string * int_expr * int_expr
  | Let_bool_int of string * bool_expr * int_expr
  | IfThenElse_int of bool_expr * int_expr * int_expr
 and bool_expr =
  | LT_bool of int_expr * int_expr
  | EQ_int_bool of int_expr * int_expr
  | EQ_bool_bool of bool_expr * bool_expr
  | And_bool of bool_expr * bool_expr
  | Not_bool of bool_expr
  | BoolConst_bool of bool
  | IfThenElse_bool of bool_expr * bool_expr * bool_expr
  | Var_bool of string
  | Let_bool_bool of string * bool_expr * bool_expr
  | Let_int_bool of string * int_expr * bool_expr

type int_or_bool_expr
  = IntExpr of int_expr 
  | BoolExpr of bool_expr 

(* Place functions eval_int_bool and translate here. *)
