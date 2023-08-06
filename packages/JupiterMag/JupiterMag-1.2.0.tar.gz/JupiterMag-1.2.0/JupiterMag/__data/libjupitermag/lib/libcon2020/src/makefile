# CFLAGS for CC
CFLAGS=-lm -fPIC -std=c++17 -Wextra -O3

# Compiler
CCo=g++ -c $(CFLAGS)
CC=g++ $(CFLAGS)
CCWo=x86_64-w64-mingw32-g++-win32 -c $(CFLAGS)
CCW=x86_64-w64-mingw32-g++-win32 $(CFLAGS)

ifndef BUILDDIR 
	BUILDDIR=../build
endif

OS=$(shell uname -s)
ifeq ($(OS),Linux)
	LIBFILE=libcon2020.so
else
	LIBFILE=libcon2020.dylib
endif

all: obj lib 

obj:
	$(CCo) con2020.cc -o $(BUILDDIR)/con2020.o 
	$(CCo) bessel.cc -o $(BUILDDIR)/bessel.o 
	$(CCo) polyeval.cc -o $(BUILDDIR)/polyeval.o 
	$(CCo) trap.cc -o $(BUILDDIR)/trap.o 
	$(CCo) smoothd.cc -o $(BUILDDIR)/smoothd.o 
	$(CCo) libcon2020.cc -o $(BUILDDIR)/libcon2020.o
	$(CCo) scalarpot.cc -o $(BUILDDIR)/scalarpot.o
	$(CCo) flux.cc -o $(BUILDDIR)/flux.o
	$(CCo) lmic.cc -o $(BUILDDIR)/lmic.o

lib:
	$(CC) $(BUILDDIR)/*.o -shared -o ../lib/$(LIBFILE)
	
winobj:
	$(CCWo) con2020.cc -o $(BUILDDIR)/con2020.o 
	$(CCWo) bessel.cc -o $(BUILDDIR)/bessel.o 
	$(CCWo) polyeval.cc -o $(BUILDDIR)/polyeval.o 
	$(CCWo) trap.cc -o $(BUILDDIR)/trap.o 
	$(CCWo) smoothd.cc -o $(BUILDDIR)/smoothd.o 
	$(CCWo) libcon2020.cc -o $(BUILDDIR)/libcon2020.o
	$(CCWo) scalarpot.cc -o $(BUILDDIR)/scalarpot.o
	$(CCWo) flux.cc -o $(BUILDDIR)/flux.o
	$(CCWo) lmic.cc -o $(BUILDDIR)/lmic.o

winlib:
	$(CCW) $(BUILDDIR)/*.o -shared -o ../lib/libcon2020.dll

test:
	$(CC) test.cc *.o -o test

