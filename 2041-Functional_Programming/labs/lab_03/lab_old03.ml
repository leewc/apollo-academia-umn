type number =  |Int  of int
	       |Float of float

let n1:number = Int 1;;
let n2:number = Int 2;;
let n4:number = Int 4;;
let n5:number = Int 5;;
let n3_1415:number = Float 3.1415;;

let to_int n = 
  match n with
  | Int n -> Some n
  | _ -> None ;;

let to_float n = 
  match n with
  | Float n -> Some n 
  | _ -> None ;;

let add_number a b = 
  match a with 
  | Int a -> match b with 
	     | Int b -> Int (a + b)
	     | Float b -> Float (float_of_int a +. b)
  | Float a -> match b with 
	       | Int b -> Float (float_of_int b +. a)
	       | Float b -> Float (a +. b)
(*
let add_number2 a b = 
  match a::b with 
  | Int a :: Int b -> Int (a + b)
(*Above fun gives error that the variant type list has no const int*)

 *)

let sub_number a b = 
  match a with 
  | Int a -> (match b with
	     | Int b -> Int (a - b)
	     | Float b -> Float(float_of_int a -. b)   )
  | Float a -> (match b with 
	       | Int b -> Float (float_of_int  a -. b)
	       | Float b -> Float ( a -. b) )
let mul_number a b = 
  match a with 
  | Int a -> match b with
	     | Int b -> Int (a * b)
	     | Float b -> Float(float_of_int a *. b)
  | Float a -> match b with 
	       | Int b -> Float (float_of_int b *. a)
	       | Float b -> Float ( a *. b)

(*
let div_number a b = 
  match a with 
  | Int a -> match b with 
	     | Int b -> if (a mod b) = 0 then Int (a /b) 
			else Float (float_of_int a /. float_of_int b)
	     | Float b -> Float (float_of_int a /. b) 
	     | Float a -> match b with *)
(*get match failure when mul num n31415 n4, basically all cases don't match the 2nd case *)
(* next just test cases for div_num *)


(* lecture code
let rec sumlist l = 
match l with 
| [] -> 0 
| (h::t) -> match h with 
	    | Int n -> n + sumlist t
	    | (Str _) -> sumlist t ;;

  *)
