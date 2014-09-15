let even n = n mod 2 = 0 ;;

let rec euclid a b =
  if a = b then a
  else if a < b then euclid a (b-a)
  else euclid (a-b) b ;;


let frac_mul (n1,d1) (n2,d2) =
  (n1*n2, d1*d2) ;;

let frac_add (n1,d1) (n2,d2) =
  (n1*d2 + n2*d1, d1*d2) ;;

let frac_simplify (n,d) =
  let rec gcd a b =
     if a = b then a
     else if a < b then gcd a (b-a)
     else gcd (a-b) b 
  in
  let div = gcd n d
  in
  (n/div, d/div) ;;

(* square root approx, assume n>1.0, real *)
let approx_squareroot acc n =
  let lower = 1.0 and upper = n
  in
  let rec sq_hlpr (low, up) =
    let guess = (up +. low) /. 2.0 in
     if (up -. low) <= acc then (low, up)
     else if (guess *. guess) > n then sq_hlpr (low, guess)
     else sq_hlpr (guess, up)
  in sq_hlpr (lower, upper) ;;

let square_approx acc n = approx_squareroot acc n;; 

(* max_list function will not work with an empty list *)
let max_list aList:int =    (*declare aList as int type *)
  let rec max a =
    match a with
    | [x] -> x
    | x::y::[] -> if x > y then x else y
    | x::y::xs -> if x > y then max (x::xs) else max (y::xs)
  in max aList  ;;

let drop d lst:int list =
  let rec drop_help d aList =
    if d = 0 then aList
    else
      match aList with
      | [] -> []
      | x::[] -> []
      | x::xs -> drop_help (d-1) xs
  in drop_help d lst  ;;

let rev lst = 
   let rec reverse alist = 
   match alist with 
   | [] -> []
   | [x] -> [x]
   | hd::tl -> (reverse tl)@[hd]
  in reverse lst

(* lol stands for list of lists *)
let is_matrix lol =
  let rec count aList n =
    match aList with
    | [] -> n
    | _::t -> count t (n+1)
  in
  let rec check l =
       match l with
       | [] -> true   (*this case doesn't reach here ... *)
       | x::[] -> true
       | x::y::[] -> if (count x 0) = (count y 0) then true else false
       | x::y::tl -> if (count x 0) = (count y 0) then check (y::tl) else false
  in check lol  ;;

(*function will only work for inputs that have is_matrix evaluated as true *)
let matrix_scalar_add lol toAdd =
  let rec add mtrix =     (*serves to add each element of matrix, internally *)
    match mtrix with
    | [] -> []
    | hd::tl -> (hd+toAdd)::(add tl)
  in
  let rec wrapper lol=
    match lol with
    | [] -> []
    | hd::tl -> (add hd)::(wrapper tl)
  in wrapper lol ;;

(* assumes that the list passed in has is_matrix evaluated as true *)
let matrix_transpose lol=
  let rec mul mtrix1 mtrix2=
    match mtrix1 with
    | [] -> []
    | hd1::tl1 -> match mtrix2 with
                 | [] -> []
                 | hd2::tl2 -> [hd1;hd2]::(mul tl1 tl2)
  in
  let rec wrapper m1=
    match m1 with
    | [] -> []
    | x::[] -> [x]
    | x::y::tl -> (mul x y)@(wrapper tl)
  in wrapper lol  ;;
(*the match in the wrapper should be @ not :: or else it becomes a list inside *)

(* A function that multiplies each respective element at the same spot *)
let matrix_multiply lol=
  let rec mul mtrix1 mtrix2=
    match mtrix1 with
    | [] -> []
    | hd1::tl1 -> match mtrix2 with
                 | [] -> []
                 | hd2::tl2 -> (hd1*hd2)::(mul tl1 tl2)
  in
  let rec wrapper m1=
    match m1 with
    | [] -> []
    | [x] -> [x]
    | x::y::tl -> (mul x y)::(wrapper tl)
  in wrapper lol ;;

(* dumb implementations due to lack of programming experience*)

(* let rec even n =
   if n = 0 then true
   else if n = 1 then false
   else even (n-2)  *)

(*
let rev lst=
  let rec count aList n =
  match aList with
  | [] -> n
  | _::t -> count t (n+1)
  in
  let c = (count lst 0) in
   let rec reverse i out c=
     match out with
     | [] -> i
     | hd::tl -> if c>0 then reverse ([hd]@i) tl (c-1) else i
   in reverse [] lst c  ;;
 *)
