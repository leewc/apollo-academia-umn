
exception KeepLooking

let show_list show l =
  let rec sl l =
    match l with 
    | [] -> ""
    | [x] -> show x
    | x::xs -> show x ^ "; " ^ sl xs
  in "[ " ^ sl l ^ " ]"

let rec foldr f v l = match l with
  | [] -> v
  | x::xs -> f x (foldr f v xs)

let is_elem v l =
  foldr (fun x in_rest -> if x = v then true else in_rest) false l

let rec map (f:'a -> 'b) (l:'a list) : 'b list =
  match l with
  | [] -> []
  | x::xs -> f x :: map f xs

let rec filter (f:'a -> bool) (l:'a list) : 'a list =
  match l with
  | [] -> []
  | x::xs -> let rest = filter f xs
	     in if f x then x :: rest else rest

let rec is_not_elem set v =
  match set with
  | [] -> true
  | s::ss -> if s = v then false else is_not_elem ss v

let rec foldl f v l = match l with
  | [] -> v
  | x::xs -> foldl f (f v x) xs
(* ###################################################### *)

(* unit -> (int * int ) list option *)
let rec generic_solver 
	  (start: (int*int)) 
	  (goal_points: (int*int) list) 
	  (movable:(int * int -> (int * int ) list)) 
	  (func:((int * int) list -> 'a option)): (int*int) list option =
 
 let rec go_from state path = 
    if is_elem state goal_points then path    (*Found goal, G, return the path found*)
    else  
      match filter (is_not_elem path) (movable state) with 
      | [] -> raise KeepLooking
      | x::xs -> (match (filter (is_not_elem path) (movable x)) with 
		    | [] -> raise KeepLooking
		    | x::xs -> (try go_from x (path@[x]) with 
				| KeepLooking -> (let hd = fun lst -> match lst with 
								    | x::xs -> x
						 in go_from (hd xs) (path@[(hd xs)]))
			       | _ -> [(100,100)])) (*something is wrong here. *)
      | _ -> []
 in Some (go_from start [start])
(*
 in try Some (go_from start [start]) with (*argument passed into go_from is the starting point, S*)
     | x -> Some x
     | KeepLooking -> (print_endline ("No other possible solutions. ")) ; None
 *)
(* int * int -> (int * int ) list*)
let maze_moves xy = 
  match xy with 
  | (1,1) -> [(2,1)]
  | (2,1) -> [(3,1);(1,1)]
  | (3,1) -> [(3,2);(2,1)]
  | (4,1) -> [(4,2)]
  | (5,1) -> [(5,2)]
  | (1,2) -> [(2,2);(1,3)]
  | (2,2) -> [(3,2);(1,2)]  
  | (3,2) -> [(2,2);(4,2);(3,1);(3,3)]
  | (4,2) -> [(3,2);(4,1)]
  | (5,2) -> [(5,1);(5,3)]
  | (1,3) -> [(1,4);(1,2);(2,3)]
  | (2,3) -> [(1,3)]
  | (3,3) -> [(3,2);(4,3);(3,4)]
  | (4,3) -> [(3,3);(5,3)]
  | (5,3) -> [(5,2);(5,4)]
  | (1,4) -> [(1,3);(1,5)]
  | (2,4) -> [(2,5);(3,4)]
  | (3,4) -> [(3,3);(2,4);(4,4)]
  | (4,4) -> [(3,4);(4,5)]
  | (5,4) -> [(5,3)]
  | (1,5) -> [(1,4);(2,5)]
  | (2,5) -> [(2,4);(1,5)]
  | (3,5) -> [(4,5)]
  | (4,5) -> [(3,5);(5,5)]
  | (5,5) -> [(4,5)]
  | _ -> [(0,0)]

let maze_gentest () = generic_solver (2,3) [(5,1);(3,5)] (maze_moves) (fun x -> Some x)

let maze_v2 (func:((int * int) list -> 'a option)): 'a option = 
  let rec go_from state path = 
    if state = (5,1) || state = (3,5) then func path    (*Found goal, G, return the path found*)
    else 
      match filter (is_not_elem path) (maze_moves state) with 
      | [] -> raise KeepLooking
      | [a] -> go_from a (path@[a])
      | [a;b] -> (try go_from a (path@[a]) with 
		  | KeepLooking -> go_from b (path@[b]) )
      | [a;b;c] -> (try go_from a (path@[a]) with 
		    | KeepLooking -> try go_from b (path@[b]) with 
				     | KeepLooking -> go_from c (path@[c]) )
      | _ -> None
  in try go_from (2,3) [(2,3)] with (*argument passed into go_from is the starting point, S*)
     | KeepLooking -> (print_endline ("No other possible solutions. ")) ; None


(* (int * int) -> string*)
let show_int_int_pair (x,y) = "(" ^ (Int.to_string x) ^ "," ^ (Int.to_string y) ^ ")" 

(* (int * int) list -> (int * int) list option *)
let rec process_solution_maze maze = 
  print_endline ("Here is a solution: " ^ show_list show_int_int_pair maze) ;
  print_endline ("Do you like it ?" ) ;
  match In_channel.input_line stdin with
  | None -> (* user typed ^D *)
     print_endline "Please enter a response."; process_solution_maze maze 
  | Some answer ->
     if is_elem 'n' (String.to_list answer) 
     then raise KeepLooking
     else (print_endline "Here's your path! " ; Some maze)



(* unit -> (int * int) list option *)
let maze_interactive () = maze_v2 process_solution_maze

(* unit -> (int * int) list option *)
let maze_first () =
  maze_v2 (fun x -> Some x)

(* unit -> 'a option*)
let maze_print_all () =
  maze_v2
    (fun x -> print_endline (show_list show_int_int_pair x) ;
          raise KeepLooking)
