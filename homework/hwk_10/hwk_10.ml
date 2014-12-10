(*Written Code - With Inspirations frm RealWorldOcaml*)
open Core.Std

(*some helper functions*)
let rec map (f:'a -> 'b) (l:'a list) : 'b list =
  match l with
  | [] -> []
  | x::xs -> f x :: map f xs

let rec foldl f v l =
  match l with
  | [] -> v
  | x::xs ->  foldl f (f v x) xs

(*Signature aka Interface for the Int/Complex Arith modules*)
module type Arithmetic_intf = sig 
    type t (*will hold interval, floats,ints, complex*)
    val to_string : t -> string
    val add : t -> t -> t
    val mul : t -> t -> t
  end

(*Int and Complex Arith Modules*)
module Int_arithmetic : (Arithmetic_intf with type t = int) = struct
  type t = int
  let to_string = Int.to_string
  let add x y = x + y
  let mul x y = x * y
end

module Complex_arithmetic : (Arithmetic_intf with type t = (float * float)) = struct
  type t = (float * float) 
  let to_string (x,y) = "(" ^ Float.to_string x ^ "+"^Float.to_string y ^"i)"
  let add (x1,y1) (x2,y2) = (x1 +. y1, x2 +. y2)   (*where y1 and y2 are the complex numbers*)
  let mul (x1,y1) (x2,y2) = ((x1 *. x2 -. y1*.y2) , (x1 *. y2 +. y1 *. x2)) 
end 

(*Signature for Int_Vector and Complex_Vector modules*)
module type Vector_intf = sig
    type t 
    type vector (*vector will either be int list or float list*)
    val create : int -> t -> vector (*the output should be abstracted, not t list*)
    val from_list : t list -> vector
    val to_list : vector -> t list
    val scalar_add : t -> vector -> vector
    val scalar_mul : t -> vector -> vector
    val scalar_prod : vector -> vector -> t option
    val to_string : vector -> string 
    val size: vector -> int

  end

(*Functor that takes in module of type Int/Complext arithmetic
  Return type is a Vector_intf type with the input type
*)
module Make_vector(Arith_mod : Arithmetic_intf) : 
    (Vector_intf with type t = Arith_mod.t) = struct
  type vector = Vector of Arith_mod.t list  (*if I do vector = Arith_mod.t it just masks it, not a good practice*)
  type t = Arith_mod.t
   
  let create (size:int) (initVal:t):vector= 
    let rec create_list (size:int) (initVal:t) = 
      if size = 0 then [] 
      else (initVal::(create_list (size-1) initVal))
    in Vector (create_list size initVal)

  let from_list (tList: t list): vector = Vector tList

  let to_list (vec: vector): t list =  match vec with Vector l -> l   

  let scalar_add (value:t) (vec:vector): vector = match vec with Vector l -> Vector (map (Arith_mod.add value) l)

  let scalar_mul (value:t) (vec:vector): vector = match vec with Vector l -> Vector (map (Arith_mod.mul value) l)
  
  let size (vec: vector): int = match vec with Vector l -> List.length l 
  
  let scalar_prod (vecA:vector) (vecB:vector): t option = 
    let rec zip (listA: t list) (listB: t list) =
      match (listA,listB) with 
      | (x::xs, y::ys) -> Arith_mod.mul x y :: zip xs ys
      | _ -> []  
    in
    let helper (vecA) (vecB) =  
      match (vecA, vecB) with 
	   | Vector a, Vector b -> match (zip a b) with
				   | x :: xs -> [foldl (Arith_mod.add) x (xs)]
				   | [] -> [] 
    in if (size vecA) <> (size vecB) then None
       else match (helper vecA vecB) with
	    | [] -> None
	    | x::xs -> Some x
 
  let to_string (vec:vector) = 
    let rec hlpr (l:t list) = 
      match l with 
      | [ ] -> " "
      | [x] -> Arith_mod.to_string x 
      | x::xs -> Arith_mod.to_string x ^ ", "^ hlpr xs
    in 
    match vec with 
    | Vector l -> "<< " ^ Int.to_string (size (vec)) ^ " | " ^ hlpr l ^ " >>" 
end 
 
module Int_vector = Make_vector(Int_arithmetic)
module Complex_vector = Make_vector(Complex_arithmetic)


(*
  Signature defining the type and ops for the numeric vals in the vector
  Modules implementing the signature wil be the input module to the functor
*)

let v1 = Int_vector.create 10 1
let v2 = Int_vector.from_list [1;2;3;4;5]
let v3 = Int_vector.scalar_add 3 v2
let v4 = Int_vector.scalar_mul 10 v2
let i1 = Int_vector.scalar_prod v3 v4
let l1 = Int_vector.to_list v3 
let i2 = Int_vector.size v4
let s1 = Int_vector.to_string v1
let s2 = Int_vector.to_string v2
let s3 = Int_vector.to_string v3
let s4 = Int_vector.to_string v4


let v5 = Complex_vector.from_list [ (1.0, 2.0); (3.0, 4.0); (5.0, 6.0) ]
let v6 = Complex_vector.scalar_add (5.0, 5.0) v5
let testmul = Complex_vector.scalar_mul (5.0, 5.0) v5
let stestmul = Complex_vector.to_string testmul
(*let c1 = Complex_vector.scalar_prod v5 v6 *)
let s5 = Complex_vector.to_string v5
let s6 = Complex_vector.to_string v6
