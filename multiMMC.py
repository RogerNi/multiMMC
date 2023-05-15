# sample usage: 
#   Calculate the accuracy using the last 10% of the data (as bytes):
#       python multiMMC.py ../state-spaces/mnist_gray.bin
#   Calculate the accuracy using the last 10% of the data (as bitstring):
#       python multiMMC.py ../state-spaces/mnist_gray.bin -b

import ctypes
import numpy as np
import argparse

parser = argparse.ArgumentParser(description='MultiMMC Python Wrapper')
parser.add_argument('filename') 
parser.add_argument('-b', '--bitstring', help='run input as bitstring', action='store_true')
args = parser.parse_args()

_multi_mmc_test = ctypes.CDLL('libMultiMMC.so')
# double multi_mmc_test(uint8_t *data, long len, int alph_size, const int verbose, const char *label, uint8_t *predictions)
_multi_mmc_test.multi_mmc_test.argtypes = (ctypes.POINTER(ctypes.c_ubyte), ctypes.c_long, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_ubyte))
_multi_mmc_test.multi_mmc_test.restype = ctypes.c_double

multi_mmc_test = _multi_mmc_test.multi_mmc_test

def infer_alpha_size(data):
    max_byte = max(data)
    return len(bin(max_byte)[2:])

def get_bitstring(data):
    return np.bitwise_and(np.expand_dims(np.frombuffer(data, dtype=np.ubyte).flatten(), 1), np.expand_dims(np.flip(2**np.arange(8), 0), 0)).__ne__(0)

if __name__ == "__main__":
    with open(args.filename, "rb") as f:
        data = f.read()
    bit_size = infer_alpha_size(data)
    alpha_size = 2**bit_size
    if args.bitstring:
        data = get_bitstring(data)
        data = data[:, -bit_size:].flatten().tobytes()
        alpha_size = 2
    print("Alpha size: ", alpha_size)
    length = len(data)
    predictions = (ctypes.c_ubyte * length)()
    data = (ctypes.c_ubyte * length).from_buffer(bytearray(data))
    verbose = 2
    label = b"test"
    multi_mmc_test(data, length, alpha_size, verbose, label, predictions)
    corrections = np.frombuffer(predictions, dtype=np.ubyte) == np.frombuffer(data, dtype=np.ubyte)
    print("Accuracy: ", np.mean(corrections[-int(length*0.1):]), f" (last 10% of data: {int(length*0.1)})")
    