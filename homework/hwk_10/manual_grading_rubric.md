# Manual grading of Homework 10


+ ?? / 5: reasonable attempt at an ``Arithmetic`` interface

+ ?? / 5: reasonable attempt at an ``Int_arithmetic`` module

+ ?? / 5: reasonable attempt at an ``Complex_arithmetic`` module

+ ?? / 5: reasonable attempt at an ``Vector`` interface

+ ?? / 5: reasonable attempt at an ``Make_vector`` functor

+ ?? / 5: reasonable attempt at an ``Int_vector`` module

+ ?? / 5: reasonable attempt at an ``Complex_vector`` module

+ ?? / 10: the type ``t`` in at least one vector module must not show the implemnetation type as a list.

  Something like the following is acceptable
   ```
   type t = Make_vector(Int_arithmetic).t in the Int_vector  
   ```         
   or
   ```     
   type t = Make_vector(Complex_arithmetic).t in the Complex_vector
   ```
