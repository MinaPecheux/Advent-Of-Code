CC = gcc
CCFLAGS = -Wall
BINDIR = ./bin/
SRCDIR = ./src/
INCDIR = ./include/
INCLUDES = -I$(INCDIR)
SRC = $(shell ls $(SRCDIR) | grep .c)
OBJ = $(patsubst %.c,%.o,$(SRC))
SRC_PREFIXED = $(patsubst %.c,$(SRCDIR)%.c,$(SRC))
OBJ_PREFIXED = $(patsubst %.c,$(BINDIR)%.o,$(SRC))
EXEC = $(shell ls $(SRCDIR) | grep day)
EXEC_PREFIXED = $(patsubst %.c,$(BINDIR)%.exe,$(EXEC))

all: $(EXEC_PREFIXED)
	
$(BINDIR)%.exe : $(BINDIR)%.o $(BINDIR)parser.o $(BINDIR)utils.o
	$(CC) $(CCFLAGS) -o $@ $< $(BINDIR)parser.o $(BINDIR)utils.o $(INCLUDES)
	
$(BINDIR)%.o : $(SRCDIR)%.c
	$(CC) $(CCFLAGS) -c $< -o $@ $(INCLUDES)

.PHONY: clean
clean:
	rm -f $(BINDIR)*.exe $(BINDIR)*.o
