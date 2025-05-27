# Compiler
CC = gcc

# Directories
SRC_DIR := .
BUILD_DIR := build
LIB_DIR := ../../build/libobj
INCLUDE_DIR := ../include

# Find all subdirectories in INCLUDE_DIR
INCLUDE_DIRS := $(shell find $(INCLUDE_DIR) -type d)
INCLUDE_FLAGS := $(addprefix -I,$(INCLUDE_DIRS))

# Target library name
LIB_NAME := j.ffmpeg
LIB_SHARED := $(LIB_DIR)/lib$(LIB_NAME).so
LIB_STATIC := $(LIB_DIR)/lib$(LIB_NAME).a

# Source and object files
SRCS := $(wildcard $(SRC_DIR)/*.c)
OBJS := $(patsubst $(SRC_DIR)/%.c, $(BUILD_DIR)/%.o, $(SRCS))

# Compiler flags
CFLAGS := -Wall -Wextra -O2 -fPIC $(INCLUDE_FLAGS)
LDFLAGS := -shared

# Default target
all: $(LIB_SHARED) $(LIB_STATIC)

# Build the shared library
$(LIB_SHARED): $(OBJS)
	@mkdir -p $(LIB_DIR)
	$(CC) $(LDFLAGS) -o $@ $^

# Build the static library
$(LIB_STATIC): $(OBJS)
	@mkdir -p $(LIB_DIR)
	ar rcs $@ $^

# Compile source files into object files
$(BUILD_DIR)/%.o: $(SRC_DIR)/%.c
	@mkdir -p $(BUILD_DIR)
	$(CC) $(CFLAGS) -c $< -o $@

# Clean build files (라이브러리 파일은 남기고 오브젝트만 삭제)
clean:
	rm -rf $(BUILD_DIR)

# 완전 정리 (오브젝트와 라이브러리 모두 삭제)
distclean:
	rm -rf $(BUILD_DIR) $(LIB_DIR)/lib$(LIB_NAME).so $(LIB_DIR)/lib$(LIB_NAME).a

.PHONY: all clean distclean