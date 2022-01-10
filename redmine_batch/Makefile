CC=gcc
CFLAGS=-g
PROG=init
DEP=common.h

all: $(PROG)

$(PROG): init.o error.o
	$(CC) $(CFLAGS) $? -o $@

init.o:	init.c
	$(CC) $(CFLAGS) -c $^

error.o: error.c
	$(CC) $(CFLAGS) -c $^

-include $(DEP)

clean:
	rm *.o
	rm $(PROG)
