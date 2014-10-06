type expr 
  = Add of  expr * expr
  | Mul of expr * expr
  | Sub of expr * expr
  | Div of expr * expr
  | Let of string * expr * expr
  | Var of string
  | LT of expr * expr (*less than*)
  | EQ of expr * expr (*equal *)
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
    | Mul (l,r) ->
        let v1 = eval_h l env  and  v2 = eval_h r env
        in (match v1,v2 with 
            | IntVal x, IntVal y -> IntVal (x * y)
            | _ -> raise (Failure "Multiplication requires 2 integer values."))
    | Sub (l,r) ->
        let v1 = eval_h l env  and  v2 = eval_h r env
        in (match v1,v2 with 
            | IntVal x, IntVal y -> IntVal (x - y)
            | _ -> raise (Failure "Subtraction requires 2 integer values."))
    | Div (l,r) ->
        let v1 = eval_h l env  and  v2 = eval_h r env
        in (match v1,v2 with 
            | IntVal x, IntVal y -> IntVal (x / y)
            | _ -> raise (Failure "Division requires 2 integer values."))
    | LT (l,r) ->
       let v1 = eval_h l env  and  v2 = eval_h r env
       in (match v1,v2 with 
            | IntVal x, IntVal y -> if x < y then BoolVal true else BoolVal false
            | _ -> raise (Failure "Less than operator requires 2 integer values."))
    | EQ (l,r) ->
       let v1 = eval_h l env  and  v2 = eval_h r env
       in (match v1,v2 with 
            | IntVal x, IntVal y -> if x = y then BoolVal true else BoolVal false
	    | BoolVal x, BoolVal y -> if x=y then BoolVal true else BoolVal false
            | _ -> raise (Failure "Equality test requires 2 values of the same type."))
    | And (l,r) ->
       let v1 = eval_h l env  and  v2 = eval_h r env
       in (match v1,v2 with 
            | BoolVal x, BoolVal y -> if x && y then BoolVal true else BoolVal false
            | _ -> raise (Failure "And operator requires 2 boolean values."))
    | Not a ->
       let v1 = eval_h a env 
       in (match v1 with 
	   | BoolVal x -> BoolVal (not x)
	   | _ -> raise (Failure "Not operator requires a boolean value."))
    | IfThenElse (b2,l,r) ->
       let b = eval_h b2 env
       in   
         (match b with 
            | BoolVal b -> if b=true then (eval_h l env) else (eval_h r env)
            | _ -> raise (Failure "If then else requires one Boolean value and 2 integer/boolean values."))
    | Let (var, def, ex) -> eval_h ex ( (var, eval_h def env)::env)
    | Var x -> lookup x env
    | IntConst v -> IntVal v
    | BoolConst b -> BoolVal b


  in eval_h e []

let freevars (a:expr):string list =
(*
  let rec inList (a:string) (b:string list) = 
    match b with 
    | x::rest -> if x = a then true else inList a rest
    | [] -> false
  in 

  let rec clean (a:string list) (refa:string list) (out:string list):string list = 
    match a with 
    | x::rest -> if not (inList x refa) then clean rest refa out@[x] else clean rest refa out
    | [] -> out
  in 
 *)
  let rec make_str (a:expr) (validate:string list):string list =
    match a with

(*    | Var x -> if not (inList x validate) then [x] else [] *)
    | Var x -> [x] 
    | Let (var,def,ex) -> (match def with
			   | IntConst _
(*
			   | BoolConst _ -> (if (inList var validate) then make_str ex validate@[var] 
					     else make_str ex validate)
 *)
			   | BoolConst _-> []
			   | _ -> [var])
    | Mul (x,y)
    | Div (x,y)
    | Sub (x,y)
    | Add (x,y) 
    | LT (x,y)
    | EQ (x,y)
    | And (x,y)
      -> make_str x validate @ make_str y validate
    | Not x -> make_str x validate
    | IfThenElse (x,y,z) -> make_str x validate @ make_str y validate @ make_str z validate
    | _ -> []
   in  
   let rec lookup n env out validate = 
    match env with 
    | [] -> out@make_str n validate
    | (name,value)::rest -> if n = name then value else lookup n rest out (validate)
   in (lookup a [] [] [])



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
