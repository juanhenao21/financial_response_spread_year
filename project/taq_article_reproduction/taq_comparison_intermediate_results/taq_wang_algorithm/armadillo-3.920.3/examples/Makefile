# NOTE:
# This file is mainly useful when doing a manual installation of Armadillo.
# It is overwritten by CMake when doing an automatic installation.
#
# You may need to edit this file to reflect the type and capabilities
# of your system.  The defaults are for a Linux system and will need
# to be changed for other systems (e.g. Mac OS X).


CXX=g++
#CXX=g++-4.2
## Under MacOS you may have an old compiler as default (e.g. GCC 4.0).
## However, GCC 4.2 or later is available and preferable due to better
## handling of template code.

#CXX=CC
## When using the Sun Studio compiler


ARMA_INCLUDE_FLAG = -I ../include
## If you've installed Armadillo's headers manually, 
## you may need to tell the compiler where they are.
## For example, change ../include to /usr/local/include
## and uncomment the above line.


#BOOST_INCLUDE_FLAG = -I /usr/include
## If you have Boost libraries, change /usr/include
## to point to where they are installed and uncomment
## the above line.


#EXTRA_LIB_FLAGS = -llapack -lblas
## The above line is an example of the extra libraries
## that can be used by Armadillo. You will also need
## to modify "include/armadillo_bits/config.hpp"
## to indicate which extra libraries are present.
## If you're using Mac OS, comment out the line and
## instead use the line below.


#EXTRA_LIB_FLAGS = -framework Accelerate
## Uncomment the above line when using Mac OS
## and modify "include/armadillo_bits/config.hpp"
## to indicate that LAPACK and BLAS libraries
## are present


#EXTRA_LIB_FLAGS = -library=sunperf
## When using the Sun Studio compiler


LIB_FLAGS = $(EXTRA_LIB_FLAGS)
## NOTE: on Ubuntu and Debian based systems you may need to add 
## -lgfortran to LIB_FLAGS


OPT = -O2
## As the Armadillo library uses recursive templates,
## compilation times depend on the level of optimisation:
##
## -O0: quick compilation, but the resulting program will be slow
## -O1: good trade-off between compilation time and execution speed
## -O2: produces programs which have almost all possible speedups,
##      but compilation takes longer


#OPT = -xO4 -xannotate=no
## When using the Sun Studio compiler


#EXTRA_OPT = -fwhole-program
## Uncomment the above line if you're compiling 
## all source files into one program in a single hit.


#DEBUG = -DARMA_EXTRA_DEBUG
## Uncomment the above line to enable low-level
## debugging.  Lots of debugging information will
## be printed when a compiled program is run.
## Please enable this option when reporting bugs.


#FINAL = -DARMA_NO_DEBUG
## Uncomment the above line to disable Armadillo's checks.
## DANGEROUS!  Not recommended unless your code has been
## thoroughly tested.


#
#
#

CXXFLAGS = $(ARMA_INCLUDE_FLAG) $(BOOST_INCLUDE_FLAG) $(DEBUG) $(FINAL) $(OPT) $(EXTRA_OPT) 

all: example1 example2

example1: example1.cpp
	$(CXX) $(CXXFLAGS)  -o $@  $<  $(LIB_FLAGS)

example2: example2.cpp
	$(CXX) $(CXXFLAGS)  -o $@  $<  $(LIB_FLAGS)


.PHONY: clean

clean:
	rm -f example1 example2

