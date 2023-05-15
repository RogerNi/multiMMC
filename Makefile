CXX := -g++
CXXFLAGS := -fPIC -shared
TARGET := libMultiMMC.so
SOURCE := multi_mmc_test.c

all:
	$(CXX) $(CXXFLAGS) -o $(TARGET) $(SOURCE)
