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

let max_number a b = 
  match (a,b) with 
  | (Float a, Float b) -> if a < b then Float b else Float a
  | (Int a, Int b) -> if a < b then Int b else Int a
  | (Int a, Float b) -> if float_of_int a > b then Int a else Float b
  | (Float a, Int b) -> if a > float_of_int b then Float a else Int b

let max_number_list l:number option=
  let rec max aList =  
    match aList with 
    | [] -> None
    | x::[] -> Some x
    | x::y::[] -> Some (max_number x y)
    | x::y::xs -> if (max_number x y) = x then max(x::xs) else max(y::xs)
  in max l
