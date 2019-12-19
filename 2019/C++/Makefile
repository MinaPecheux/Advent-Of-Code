CC = g++
CCFLAGS = -std=c++11 -Wall
BINDIR = ./bin/
SRCDIR = ./src/
INCDIR = ./include/
INCLUDES = -I$(INCDIR)
SRC = $(shell ls $(SRCDIR) | grep .cpp)
OBJ = $(patsubst %.cpp,%.o,$(SRC))
SRC_PREFIXED = $(patsubst %.cpp,$(SRCDIR)%.cpp,$(SRC))
OBJ_PREFIXED = $(patsubst %.cpp,$(BINDIR)%.o,$(SRC))
EXEC = $(shell ls $(SRCDIR) | grep day)
EXEC_PREFIXED = $(patsubst %.cpp,$(BINDIR)%.exe,$(EXEC))

all: $(EXEC_PREFIXED)
	
$(BINDIR)%.exe : $(BINDIR)%.o $(BINDIR)parser.o $(BINDIR)utils.o
	@echo ">>> Building files..."
	@mkdir -p $(BUILDDIR)/$(notdir $(patsubst %/,%,$(dir $<)))
	$(CC) $(CCFLAGS) -o $@ $< $(BINDIR)parser.o $(BINDIR)utils.o $(INCLUDES)
	
$(BINDIR)%.o : $(SRCDIR)%.cpp
	@echo ">>> Linking..."
	@mkdir -p $(BINDIR)
	$(CC) $(CCFLAGS) -c $< -o $@ $(INCLUDES)

.PHONY: clean
clean:
	@echo ">>> Cleaning...";
	rm -f $(BINDIR)*.exe $(BINDIR)*.o
	rm -rf $(BINDIR)*.exe.dSYM
