.PHONY: all clean

LIB_PATH = ../build/libobj
LIB_FLAGS = -lj.file
BUILD_DIR = ../build/bin
TARGET = $(BUILD_DIR)/incoming

SRCS = $(wildcard *.c)
CFLAGS = -Wall -pthread -I$(INCLUDE_FLAGS)
INCLUDE_DIR = ../libj/include

# Find all subdirectories in INCLUDE_DIR
INCLUDE_DIRS = $(shell find $(INCLUDE_DIR) -type d)
INCLUDE_FLAGS = $(addprefix -I,$(INCLUDE_DIRS))

all: $(TARGET)

$(TARGET): $(SRCS)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) -o $@ $^ -L$(LIB_PATH) $(LIB_FLAGS)

clean:
	rm -f $(TARGET)