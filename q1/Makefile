#makefile maybe used

SRC = something.py
TARGET = something.pyc
BOOL_EXP = ques.txt

CUR_DIR = $(shell pwd)
BUILD_DIR = $(CUR_DIR)/build

.phony: all build clean 

all: clean build

clean:
	rm -rf $(BUILD_DIR)

build:
	mkdir -p $(BUILD_DIR)
	python3 $(SRC) --output $(BUILD_DIR)/$(TARGET)