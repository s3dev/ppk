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
# 0.2.0.dev1:
#   Updated to include a 'dev' mode which adds debugging symbols, sets the
#   __DEV_MODE macro and does not optimise. If the flag is missing, 
#   optimisation is set at O3.
#   Invoked as: make MODE=dev
#

IGNORE = -Wno-unused-variable -Wno-deprecated-declarations
CFLAGS = -Wall -Werror -Wextra -Wpedantic -Wshadow -std=gnu11 $(IGNORE)

TARGET = upack
CC = gcc
LDFLAGS = -static -lcrypto
LIBS =
SOURCES = %.c
OBJECTS = $(patsubst %.c, %.o, $(wildcard *.c))
HEADERS = $(wildcard *.h)

# Switch into development mode. Invoked with: $ make MODE=dev
ifeq ($(MODE),dev)
    CFLAGS += -g -D __DEV_MODE -O0
else
    CFLAGS += -O3
endif
# Add debugging symbols. Invoked with: $ make DEBUG=y
ifeq ($(DEBUG),y)
    CFLAGS += -g
endif

all: default
default: $(TARGET)

# Create the executable from the object files.
$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) $(OBJECTS) $(LDFLAGS) -o $@
	rm *.o
	rm ../bin/upack
	ln -s ../src/upack ../bin/upack

# Compile all needed source files.
%.o: %.c $(HEADERS)
	$(CC) $(CFLAGS) -c $< -o $@

# The 'clean' target definition.
.PHONY: clean
clean:
	-rm -f $(TARGET)
	-rm -f *.o

# File dependencies.
checks.o: base.h  filesys.o ui.o utils.o
filesys.o: base.h ui.o utils.o
ui.o: base.h
upack.o: base.h checks.o filesys.o ui.o utils.o
utils.o: base.h
