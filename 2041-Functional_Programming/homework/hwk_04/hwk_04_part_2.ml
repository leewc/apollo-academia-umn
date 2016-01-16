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
     (* given: | Let (a,b,c) -> (a,(eval_h b env))::env  ~then we do~ eval_h c ((a,(eval_h n env))::env)       *)
    | Var x -> lookup x env
    | IntConst v -> IntVal v
    | BoolConst b -> BoolVal b


  in eval_h e []

let freevars (e:expr) : string list =
  let rec present s env = match env with
                          | [] -> false
                          | x::xs -> x=s || (present s xs)
                          (*right side is not evaluated if left is true*)
  in 
  let rec freevars_h e env:string list = 
    match e with
    | IntConst _ -> []
    | BoolConst _ -> []
    | Var x -> if present x env then [] else [x] (*need a recursive helper function to check if it's been def*)
    | Sub (x,y)
    | Add (x,y) 
    | Mul (x,y)
    | Div (x,y) 
    | LT (x,y)
    | EQ (x,y)
    | And (x,y) -> (freevars_h x env) @ (freevars_h y env)
    | Not x -> freevars_h x env
    | IfThenElse (x,y,z) -> (freevars_h x env) @ (freevars_h y env) @ (freevars_h z env)
    | Let (x,y,z) -> (freevars_h y env) @ (freevars_h z (x::env))
  in freevars_h e []

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
type vartype = IntType | BoolType | ErrorType

let translate (e:expr) : int_or_bool_expr option = 
  let rec lookup n env = match env with 
    | [ ] -> None
    | (name, value)::rest -> if n=name then Some value else lookup n rest 
  in 
  let rec translate_h e env = match e with 
    | IntConst x -> Some (IntExpr (IntConst_int x))
    | BoolConst x -> Some (BoolExpr (BoolConst_bool x))
    | Var x -> (match lookup x env with 
		| Some IntType -> Some (IntExpr (Var_int x))
		| Some BoolType -> Some (BoolExpr (Var_bool x))
		| Some ErrorType -> None
		| None -> None )
    | Add (x,y) -> (match translate_h x env, translate_h y env with 
		    | Some (IntExpr a), Some (IntExpr b) -> Some (IntExpr (Add_int (a,b)))
		    | _,_ -> None)
    | Sub (x,y) -> (match translate_h x env, translate_h y env with 
		    | Some (IntExpr a), Some (IntExpr b) -> Some (IntExpr (Sub_int (a,b)))
		    | _,_ -> None)
    | Div (x,y) -> (match translate_h x env, translate_h y env with 
		    | Some (IntExpr a), Some (IntExpr b) -> Some (IntExpr (Div_int (a,b)))
		    | _,_ -> None)
    | Mul (x,y) -> (match translate_h x env, translate_h y env with 
		    | Some (IntExpr a), Some (IntExpr b) -> Some (IntExpr (Mul_int (a,b)))
		    | _,_ -> None)
    | LT (x,y) -> (match translate_h x env, translate_h y env with 
		    | Some (IntExpr a), Some (IntExpr b) -> Some (BoolExpr (LT_bool (a,b)))
		    | _,_ -> None)
    | EQ (x,y) -> (match translate_h x env, translate_h y env with 
		    | Some (IntExpr a), Some (IntExpr b) -> Some (BoolExpr (EQ_int_bool (a,b)))
		    | Some (BoolExpr a), Some (BoolExpr b) -> Some (BoolExpr (EQ_bool_bool (a,b)))
		    | _,_ -> None)
    | And (x,y) -> (match translate_h x env, translate_h y env with 
		    | Some (BoolExpr a), Some (BoolExpr b) -> Some (BoolExpr (And_bool (a,b)))
		    | _,_ -> None)
    | Not (x) -> (match translate_h x env with
		  | Some (BoolExpr x) -> Some (BoolExpr (Not_bool x))
		  | _ -> None )
    | IfThenElse (x,y,z) -> (match translate_h x env with 
			     | Some (BoolExpr a) -> (match translate_h y env with 
						     | Some (IntExpr b) -> (match translate_h z env with
									    | Some (IntExpr c) -> Some (IntExpr (IfThenElse_int (a,b,c)))
									    | _ -> None)
						     | Some (BoolExpr b) -> (match translate_h z env with 
									     | Some (BoolExpr c) -> Some (BoolExpr (IfThenElse_bool(a,b,c)))
									     | _ -> None)
						     | _ -> None) 
			     | _ -> None)
    | Let (x,y,z) -> (match translate_h y env with 
		      | Some (IntExpr a) -> (match translate_h z ((x,IntType)::env) with 
					     | Some (IntExpr b) -> Some (IntExpr (Let_int_int (x,a,b)))
					     | Some (BoolExpr b) -> Some (BoolExpr (Let_int_bool (x,a,b)))
					     | None -> None )
		      | Some (BoolExpr a) -> (match translate_h z ((x,BoolType)::env) with 
					      | Some (IntExpr b) -> Some (IntExpr (Let_bool_int (x,a,b)))
					      | Some (BoolExpr b) -> Some (BoolExpr (Let_bool_bool (x,a,b)))
					      | None -> None)
		      | _-> (match translate_h z ((x,ErrorType)::env) with
			     | _ -> None)
		     )
  in translate_h e []


let eval_int_bool (w:int_or_bool_expr):value = 
 
  let rec lookup n env=
    match env with
    | [ ] -> raise (Failure ("Identifier \"" ^ n ^ "\" not declared."))
    | (name,value)::rest -> if n = name then value else lookup n rest
  in 

  let rec i (x) (envI) (envB)= 
    match x with
    | IntConst_int d -> d
    | Add_int (a,b) -> (i a envI envB) + (i b envI envB)
    | Sub_int (a,b) -> (i a envI envB) - (i b envI envB)
    | Mul_int (a,b) -> (i a envI envB) * (i b envI envB)
    | Div_int (a,b) -> (i a envI envB) / (i b envI envB)
    | IfThenElse_int (a,c,d) -> if (b a envI envB) then (i c envI envB) else (i d envI envB)
    | Let_int_int (var,def,ex) -> (i ex ((var, (i def envI envB)):: envI) envB)
    | Let_bool_int (var,def,ex) -> (i ex envI ((var, (b def envI envB)):: envB))
    | Var_int a -> (lookup a envI)
  and b (y) (envI) (envB) =
    match y with 
    | BoolConst_bool d -> d
   | LT_bool (d,e) -> (i d envI envB) < (i e envI envB)
    | EQ_int_bool (d,e) -> (i d envI envB) = (i e envI envB)
    | EQ_bool_bool (d,e) -> (b d envI envB) = (b e envI envB)
    | And_bool (d,e) -> (b d envI envB) && (b e envI envB)
    | Not_bool d -> not (b d envI envB)
    | Let_bool_bool (var,def,ex) -> (b ex envI ((var, (b def envI envB))::envB))
    | Let_int_bool (var,def,ex) -> (b ex ((var,(i def envI envB)):: envI) envB)
    | Var_bool d -> (lookup d envB)
    | IfThenElse_bool (c,d,e) -> if (b c envI envB) then (b d envI envB) else (b e envI envB)
  in 
  match w with 
  | IntExpr x -> IntVal (i x [] [])
  | BoolExpr x -> BoolVal (b x [] [])

(*fail at: eval_int_bool (IntExpr (Add_int (IntConst_int 4, (Add_int (IntConst_int 1, IntConst_int 2)))));;
eval_int_bool (IntExpr (Add_int (IntConst_int 4, (Add_int (IntConst_int 1, IntConst_int 2)))));;
*)

