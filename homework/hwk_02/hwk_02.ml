let even n = n mod 2 = 0 ;;

let rec euclid a b =
  if a = b then a
  else if a < b then euclid a (b-a)
  else euclid (a-b) b


let frac_mul (n1,d1) (n2,d2) =
  (n1*n2, d1*d2)

let frac_add (n1,d1) (n2,d2) =
  (n1*d2 + n2*d1, d1*d2)

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
let square_approx acc n =
  let lower = 1.0 and upper = n
  in
  let rec sq_hlpr (low, up) =
    let guess = (up +. low) /. 2.0 in
     if (up -. low) <= acc then (low, up)
     else if (guess *. guess) > n then sq_hlpr (low, guess)
     else sq_hlpr (guess, up)
  in sq_hlpr (lower, upper) ;;

(* max_list function will not work with an empty list *)
let max_list aList =
  let rec max a =
    match a with
    | [x] -> x
    | x::y::[] -> if x > y then x else y
    | x::y::xs -> if x > y then max (x::xs) else max (y::xs)
  in max aList

let drop d lst =
  let rec drop_help d aList =
    if d = 0 then aList
    else
      match aList with
      | [] -> []
      | x::[] -> []
      | x::xs -> drop_help (d-1) xs
  in drop_help d lst

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
   in reverse [] lst c





(* let rec even n =
   if n = 0 then true
   else if n = 1 then false
   else even (n-2)  *)





