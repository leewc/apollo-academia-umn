type number =  |Int  of int
	       |Float of float

let n1:number = Int 1;;
let n2:number = Int 2;;
let n4:number = Int 4;;
let n5:number = Int 5;;
let n3_1415:number = Float 3.1415;;

(* number -> int option*)
(* converts a number type to an int type if it is of type int *)
let to_int: (number -> int option) = function
  | Int n -> Some n
  | _ -> None ;;

(*option is type cons so float option as we return an option of float *)
(* number -> float option means it takes a number function and returns float option *)

(* number -> float option*)
(* converts a number type to a float type if it is of type float*)
let to_float: (number -> float option) = function
  | Float n -> Some n
  | _ -> None ;;

(* number -> number -> number *)
(* adds 2 numbers based on which type it is and returns the correct type.
   Any Float types in the numbers will return a Float type, converts an
   int to float *)
let add_number (a:number) (b:number) :number =
  match (a,b) with  
  | (Int a, Int b) -> Int (a+b) 
  | (Float a, Int b) -> Float (a +. float_of_int b)
  | (Int a, Float b) -> Float (float_of_int a +. b)
  | (Float a, Float b) -> Float ( a +. b)

(* number -> number -> number *)
(* subtracts 2 numbers based on which type it is and returns the correct 
   type. Any Float types in the numbers will return a Float type, converts an int to float *)
let sub_number (a:number) (b:number) :number =
  match (a,b) with 
  | (Int a, Int b) -> Int (a-b)
  | (Int a, Float b) -> Float (float_of_int a -. b)
  | (Float a, Int b) -> Float (a -. float_of_int b)
  | (Float a, Float b) -> Float (a -. b)


(* number -> number -> number *)
(* multiplies 2 numbers based on which type it is and returns the correct
   type. Any Float types in the numbers will return a Float type, converts
   an int to float *)
let mul_number (a:number) (b:number): number =
  match(a,b) with 
  | (Int a, Int b) -> Int (a*b)
  | (Int a, Float b) -> Float (float_of_int a *. b)
  | (Float a, Int b) -> Float (a *. float_of_int b)
  | (Float a, Float b) -> Float (a *. b)


(* number -> number -> number *)
(* divides 2 numbers based on which type it is and returns the correct
   type. If any numbers contain a float, a float type is returned where the int type is also converted to a float. Also, if 2 Int types are passed in, the function returns a dividend of Int type if both numbers are completely divisible, oe else a function type returns when the numbers have flaoting point values when returned. *)
let div_number (a:number) (b:number): number =
 match (a,b) with 
 | (Int a, Int b) -> if (a mod b) = 0 then Int (a/b) 
		     else Float (float_of_int a /. float_of_int b)
 | (Int a, Float b) -> Float (float_of_int a /. b)
 | (Float a, Int b) -> Float (a /. float_of_int b)
 | (Float a, Float b) -> Float (a /. b) 
