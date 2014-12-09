(*Written Code - With Inspirations frm RealWorldOcaml*)

(*Signature for the vector modules*)
module type Arithmetic_intf = sig 
    type t (*will hold interval, floats,ints, complex*)
    val to_string : t -> string
  end

(*Functor for creating vector modules above*)

(*
  Signature defining the type and ops for the numeric vals in the vector
  Modules implementing the signature wil be the input module to the functor
*)
