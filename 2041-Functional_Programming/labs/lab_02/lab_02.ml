(* uses diameter to calculate area *)
let circle_area_v1 d = (d *. d) *. 3.1415 /. 4.0

(* makes use of a nested let expression *)
let circle_area_v2 d =
  let radius = d /. 2.0 and pi = 3.1415 in 
     radius *. radius *. pi

(* computes everything in the list *)
let rec product alist = 
  match alist with 
  | [] -> 0
  | [x] -> x
  | x::rest -> x * product rest

(* compute sum of differences for a list size of >=2 *)
let rec sum_diffs alist = 
  match alist with
  | [] -> 0
  | x::(y::[]) -> x - y
  | x::y::rest -> x - y + sum_diffs (y::rest) (*need to pass y::rest to sum_diffs or else won't be successive*)

(* 2D points and compute distance *)
let distance (x1,y1) (x2,y2) = 
  sqrt((y2-.y1)**2.0 +. (x2-.x1) **2.0)
  
let triangle_perimeter (x1,y1) (x2,y2) (x3,y3) = 
  distance (x1,y1) (x2,y2) +. distance (x2,y2) (x3,y3) +. distance (x3,y3) (x1, y1)

let perimeter thelist = 
  let first thelist = 
    match thelist with
    | [] -> (0.0, 0.0)   (*have to return tuple to distance*)
    | head::_ -> head
  in 
  let rec p_helper alist = 
    match alist with
    | [] -> 0.0 (*cannot be just 0 or else Ocaml thinks it's an int*)
    | [x] -> distance (first thelist) x
     (* wrong case~ x::y::z::[] -> (distance x y) +. (distance y z) +. (distance z x) *)
    | x::y::rest ->  distance x y +. p_helper (y::rest)        (*wrong~ +. distance (first alist) y *)
  in p_helper thelist

