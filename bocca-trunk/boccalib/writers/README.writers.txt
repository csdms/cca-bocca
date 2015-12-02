Trivia that makes some things the way they are:

*) Do not declare local variables in f90 that are likely to conflict with sidl function names.
A specific example: a method in a port named integrate() and the user making a port named 'integrate'.
Declaring a local variable for the port with the same name is fine in c++ and fatal in f90 with the
way use works. For f90, something sidl impossible would be $portname + '__p'. note the __ which
shouldn't come from sidl-generated symbols.

*) In C/c++/java/python, declare class instance data members starting with d_ for one-offs and
other more specific prefix/suffix for related groups. 
An example list: d_services, d_pptm_$portname (typemap for a parameter port)
