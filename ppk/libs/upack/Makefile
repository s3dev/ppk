#
# Makefile for the ppk project's upack program.
#
# Ref: https://www3.ntu.edu.sg/home/ehchua/programming/cpp/gcc_make.html#zz-2.
#
# 0.1.0.dev4:
#   CFLAGS changed to -std=gnu11 (from gnu17) in order to build on Debian 
#   buster for AI cluster support.
#   Found while recompiling to use openssl v1.1.1, as v3+ which was compiled
#   on LTP01 would not run due to the missing shared library.
#
# 0.1.0.dev5:
#   Updated to statically link the libraries.
#   Initially, only libcrypto was statically linked, however it needs 
#   libc.so.6 (GLIBC v2.34). Where the cluster has v2.27.
#   Therefore, all libraries are statically linked. The executable remains
#   relatively small, so this is acceptable.
#

IGNORE = -Wno-unused-variable -Wno-deprecated-declarations
CFLAGS = -Wall -Werror -Wextra -Wpedantic -Wshadow -O2 -std=gnu11 $(IGNORE)

TARGET = upack
CC = gcc
LDFLAGS = -static -lcrypto
LIBS =
SOURCES = %.c
OBJECTS = $(patsubst %.c, %.o, $(wildcard *.c))
HEADERS = $(wildcard *.h)

default: $(TARGET)
all: default

# Compile all needed source files.
%.o: %.c $(HEADERS)
	$(CC) $(CFLAGS) -c $< -o $@

# Create the executable from the object files.
$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) $(OBJECTS) $(LDFLAGS) -o $@
	rm *.o

# The 'clean' target definition.
.PHONY: clean
clean:
	-rm -f $(EXE)
	-rm -f *.o

# File dependencies.
checks.o: base.h  filesys.o ui.o utils.o
filesys.o: base.h ui.o utils.o
ui.o: base.h
upack.o: base.h checks.o filesys.o ui.o utils.o
utils.o: base.h

