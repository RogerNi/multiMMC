CXX := g++
CXXFLAGS := -fPIC -shared
TARGET := libMultiMMC
SOURCE := multi_mmc_test_dxx.c

all:
	# $(CXX) $(CXXFLAGS) -o $(TARGET) $(SOURCE)
	for d_mmc in 8 16 32 64 96 ; do \
		$(CXX) $(CXXFLAGS) -DD_MMC=$$d_mmc -o $(TARGET)$$d_mmc.so $(SOURCE) ; \
	done

clean:
	for d_mmc in 8 16 32 64 96 ; do \
		rm -f $(TARGET)$$d_mmc; \
	done