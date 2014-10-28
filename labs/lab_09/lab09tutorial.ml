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
  in let(_, l1, l2) = foldl f (true,[],[]) ls in (l1,l2) (*the _ in the first let _ is for the which variable which we don't need*)
  (*basically we 'initialize' values by passing it in initially*)


(* the let _ in (_,_) function behavior is the same as:
    let x = 5 in x 
    let x,y = 5,6 in x
    let x::xs = [1;2] in x 
*)

(*HINT: we want to pass in a list of list as a value in the tuple and then only finally return that*)
