====================
 Non-approved ideas
====================

The following are just ideas which I think we should consider at some point.
I've just collected a small rationale for each.  There are competing ideas;
doing one would most like hinder another.


Compile to native code (with LLVM)
==================================

We could try to compile a whole program to LLVM as a JIT.  This requires the
demand to:

a) either have a compile-time known memory layout (static typing)

b) provide a sort of FFI for our program.

   In this case, we'll still regard demands as immutable, and try to request a
   foreign value only once.

This requires a lot of effort and if programs are not kept in memory for long
the overhead of compilation with LLVM may be noticeable and overcome the any
speed up obtained.

Speed up computation of tables by converting to self-adjusting programs
=======================================================================

Price tables are computed by changing the input to the program one attribute
at a time.  This suggest that instead of performing the entire computation we
could just perform a small amount of it if we know how the changed attribute
is used in the program.

This is the subject of PhD thesis by Umut A. Acar, `Self-Adjusting Computation
<https://bok.merchise.org/book/1030>`__, which has been already
`implemented for OCaml <https://opensource.janestreet.com/incremental/>`__.

This might only be necessary for very large programs with very large price
tables.
