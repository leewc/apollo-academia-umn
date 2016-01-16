(*
Const int n=7

int ls[n]
int a[(n+1)/2];
int b[n/2];
bool which = true;
int ai=0 bi=0;
for (int i=0; i < n; i++) {
   if(which) {
       a[ai++] = ls[i] 
   }
   else { 
      b[bi++] = ls[i];

   }
   which = !which;

*)

(* //this is without the use of foldl *)
let everyotherNoFold ls =
  let f(l1,l2) x which = 
    if which then (l1 @ [x], l2) else (l1, l2 @ [x])
  in 
  let rec helper v l which =  (*v is a tuple!*) 
    match l with 
    | [] -> v
    | x::xs -> helper ( f v x which) xs (not which)
  in helper ([], []) ls true



(*foldl does not allow us to hold on to true/false
   we do this by folding into something that has the value, basically the use of a tuple
*)
let everyotherStillNoFold ls =
  let f(which,l1,l2) x = 
    if which then (false, l1 @ [x], l2) else (true, l1, l2 @ [x])
  in 
  let rec helper v l = 
    match l with 
    | [] -> v
    | x::xs -> helper (f v x) xs
  in let(_, l1,l2) = helper (true,[],[]) ls in (l1,l2)


(* equivalent javacode
Const int n=7

int ls[n]
int a[(n+1)/2];
int b[n/2];
bool which = true;
int ai=0 bi=0;
for (int i=0; i < n; i++) {
   if(which) {
       a[ai++] = ls[i]; which = false;
   }
   else { 
      b[bi++] = ls[i]; which = true;
   }
*)

let rec foldl f v l = 
  match l with
  | [] -> v
  | x::xs -> foldl f (f v x) xs

let everyother ls =
  let f (which, l1,l2) x = 
    if which then (false, l1 @ [x],l2) 
    else (true, l1,l2@[x])
  in let(which, l1, l2) = foldl f (true,[],[]) ls in (l1,l2) (*the _ in the first let _ is for the which variable which we don't need*)
  (*basically we 'initialize' values by passing it in initially*)


(* the let _ in (_,_) function behavior is the same as:
    let x = 5 in x 
    let x,y = 5,6 in x
    let x::xs = [1;2] in x 
*)

(*HINT: we want to pass in a list of list as a value in the tuple and then only finally return that*)


(*EXPERIMENTAL CODE MADE FOR HOMEWORK 6*)

(*does not take an eq func, and also exhibits wrong behaviour*)
let test (ls:'a list) (kill:'a list)=
  let ab = (fun x -> fun c -> x = c) in
  let f (ab,l1,l2,kill) x = 
    match kill with 
    | k::ks -> if ab k x then (ab, l1@[l2],[], ks) 
			    else (ab,l1,l2@[x],kill)
    | [] -> (ab,l1@[l2@[x]],l2,[])
  in let(ab, l1, l2,kill) = foldl f (ab,[[]],[],kill) ls in l1


let rec filter (f:'a -> bool) (l:'a list) : 'a list =
  match l with
  | [] -> []
  | x::xs -> let rest = filter f xs
	     in if f x then x :: rest else rest

let is_elem (a:'a) (lst: 'a list):bool = 
  match (filter (fun b -> if b=a then true else false) lst) with
  | [] -> false
  | _ -> true

(*
let test2 (eq:'a-> 'a -> bool) (ls: 'a list) (kill: 'a list) = 
  let eo (switch, (lista: 'a list list), (listb: 'a list)) (e:'a) = 
    let ab =foldl (fun x -> fun c -> x = c) e kill in
    match ab with
    | true -> (ab, lista@[listb], [])
    | false -> (ab, lista, listb@[e])
  in let(_,l1,l2) = foldl eo (false,[],[]) ls in l1@[l2]
 *)
(*was foldl ab e kill*)
(*something is wrong with e!!! the type is bool and didnt show as int*)

(* test3 uses is_elem and ignore the eq function! *)
let test3 (eq:'a -> 'a -> bool) (ls: 'a list) (kill: 'a list) = 
  let eo (switch, (lista: 'a list list), (listb: 'a list)) (e:'a) = 
    match (is_elem e kill) with
    | true -> (is_elem e kill, lista@[listb], [])
    | false -> (is_elem e kill, lista, listb@[e])
  in let(_,l1,l2) = foldl eo (false,[],[]) ls in l1@[l2]


(*test 4 successfully implements the eq function*)
let test4 (eq:'a -> 'a -> bool) (ls: 'a list) (kill: 'a list) = 
  let aux (a:'a) (lst: 'a list):bool = 
  match (filter (fun b -> if (eq b a) then true else false) lst) with
  | [] -> false
  | _ -> true
  in 
  let eo ((lista: 'a list list), (listb: 'a list)) (e:'a) = 
    match (aux e kill) with
    | true -> (lista@[listb], [])
    | false -> (lista, listb@[e])
  in let(l1,l2) = foldl eo ([],[]) ls in l1@[l2]

(*test 5 does not accept the right type, unable to collapse the aux fun*)
let test5 (eq:'a -> 'a -> bool) (ls: 'a list) (kill: 'a list) = 
  let aux (a:'a) (lst: 'a list):bool = foldl eq a lst
  in 
  let eo ((lista: 'a list list), (listb: 'a list)) (e:'a) = 
    match (aux e kill) with
    | true -> (lista@[listb], [])
    | false -> (lista, listb@[e])
  in let(l1,l2) = foldl eo ([],[]) ls in l1@[l2]
