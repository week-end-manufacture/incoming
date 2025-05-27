.PHONY: all clean

LIB_PATH = ../build/libobj
LIB_FLAGS = -lj.file \
			-lj.env
BUILD_DIR = ../build/bin
TARGET = $(BUILD_DIR)/incoming

INCLUDE_DIR = ../libj/include

# Find all subdirectories in INCLUDE_DIR
INCLUDE_DIRS = $(shell find $(INCLUDE_DIR) -type d)
INCLUDE_FLAGS = $(addprefix -I,$(INCLUDE_DIRS))

SRCS = $(wildcard *.c)
CFLAGS = -Wall -pthread -I$(INCLUDE_FLAGS)

all: $(TARGET)

$(TARGET): $(SRCS)
	mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) -o $@ $^ -L$(LIB_PATH) $(LIB_FLAGS)

clean:
	rm -f $(TARGET)

distclean:
	rm -rf $(BUILD_DIR)