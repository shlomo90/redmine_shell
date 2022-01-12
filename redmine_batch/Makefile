CC=gcc
CFLAGS=-g
PROG=red_init
DEP=red_common.h

all:	$(PROG)

$(PROG):		red_init.o red_error.o red_server.o
	$(CC) $(CFLAGS) $? -o $@

red_init.o:		red_init.c
	$(CC) $(CFLAGS) -c $^

red_error.o:	red_error.c
	$(CC) $(CFLAGS) -c $^

red_server.o:	red_server.c
	$(CC) $(CFLAGS) -c $^

clean:
	rm *.o
	rm $(PROG)
