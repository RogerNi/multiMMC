# sample usage: 
#   Calculate the accuracy using the last 10% of the data (as bytes):
#       python multiMMC.py ../state-spaces/mnist_gray.bin
#   Calculate the accuracy using the last 10% of the data (as bitstring):
#       python multiMMC.py ../state-spaces/mnist_gray.bin -b

import ctypes
import numpy as np
import argparse
import os

D_MMCs = [8, 16, 32, 64, 96]

parser = argparse.ArgumentParser(description='MultiMMC Python Wrapper')
parser.add_argument('-f', '--files', nargs='+', help='files to test', required=True) 
parser.add_argument('-u', '--human', help='human readable', action='store_true')
parser.add_argument('-d', '--dataset', help='override dataset name')
parser.add_argument('-c', '--color', help='override color name')
args = parser.parse_args()

predictors = []

for d_mmc in D_MMCs:
    _multi_mmc_test = ctypes.CDLL(os.path.join(os.path.dirname(__file__), f'libMultiMMC{d_mmc}.so'))
    # double multi_mmc_test(uint8_t *data, long len, int alph_size, const int verbose, const char *label, uint8_t *predictions)
    _multi_mmc_test.multi_mmc_test.argtypes = (ctypes.POINTER(ctypes.c_ubyte), ctypes.c_long, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.POINTER(ctypes.c_ubyte), ctypes.POINTER(ctypes.c_bool))
    _multi_mmc_test.multi_mmc_test.restype = ctypes.c_double
    multi_mmc_test = _multi_mmc_test.multi_mmc_test
    predictors.append(multi_mmc_test)

def infer_alpha_size(data):
    max_byte = max(data)
    return len(bin(max_byte)[2:])

def get_bitstring(data):
    return np.bitwise_and(np.expand_dims(np.frombuffer(data, dtype=np.ubyte).flatten(), 1), np.expand_dims(np.flip(2**np.arange(8), 0), 0)).__ne__(0)

def infer_dataset(filename):
    color = ''
    data = ''
    if 'mnist' in filename.lower():
        data = 'mnist'
    elif 'cifar' in filename.lower():
        data = 'cifar10'
    if 'gray' in filename.lower():
        color = 'grayscale'
    elif 'bw' in filename.lower():
        color = 'bw'
    if args.dataset:
        data = args.dataset
    if args.color:
        color = args.color
    return color, data

def last_byte_predictor_acc(data):
    length = len(data)
    predictions = np.insert(data, 0, 0)[:length]
    corrections = predictions == np.frombuffer(data, dtype=np.ubyte)
    return  np.mean(corrections[-int(length*0.1):])
    
def byte_acc(file, predictor):
    with open(file, "rb") as f:
        data = f.read()
    bit_size = infer_alpha_size(data)
    alpha_size = 2**bit_size
    length = len(data)
    predictions = (ctypes.c_ubyte * length)()
    predicted = (ctypes.c_bool * length)()
    data = (ctypes.c_ubyte * length).from_buffer(bytearray(data))
    verbose = 0
    label = b"test"
    predictor(data, length, alpha_size, verbose, label, predictions, predicted)
    corrections = (np.frombuffer(predictions, dtype=np.ubyte) == np.frombuffer(data, dtype=np.ubyte)) * np.frombuffer(predicted, dtype=bool)
    return  np.mean(corrections[-int(length*0.1):]), data

def bit_acc(file, predictor):
    with open(file, "rb") as f:
        data = f.read()
    bit_size = infer_alpha_size(data)
    alpha_size = 2**bit_size
    data = get_bitstring(data)
    data = data[:, -bit_size:].flatten().tobytes()
    alpha_size = 2
    length = len(data)
    predictions = (ctypes.c_ubyte * length)()
    predicted = (ctypes.c_bool * length)()
    data = (ctypes.c_ubyte * length).from_buffer(bytearray(data))
    verbose = 0
    label = b"test"
    predictor(data, length, alpha_size, verbose, label, predictions, predicted)
    corrections = (np.frombuffer(predictions, dtype=np.ubyte) == np.frombuffer(data, dtype=np.ubyte)) * np.frombuffer(predicted, dtype=bool)
    return  np.mean(corrections[-int(length*0.1):]), data

if __name__ == "__main__":
    for f in args.files:
        last_bit_acc = 0
        last_byte_acc = 0
        for i in range(len(predictors)):
            bit_a, bit_data = bit_acc(f, predictors[i])
            byte_a, byte_data = byte_acc(f, predictors[i])
            if args.human:
                print(f'MutliMMC{D_MMCs[i]}', *infer_dataset(os.path.basename(f)), f": Bit Accuracy: {bit_a}, Byte Accuracy: {byte_a}")
                if i == 0:
                    print('LastSample', *infer_dataset(os.path.basename(f)), f": Bit Accuracy: {last_byte_predictor_acc(bit_data)}, Byte Accuracy: {last_byte_predictor_acc(byte_data)}")
            else:
                print(f'MutliMMC{D_MMCs[i]}', *infer_dataset(os.path.basename(f)), bit_a, byte_a, 0, 0, sep='\t')
                if i == 0:
                    print('LastSample', *infer_dataset(os.path.basename(f)), last_byte_predictor_acc(bit_data), last_byte_predictor_acc(byte_data), 0, 0, sep='\t')
            if bit_a == last_bit_acc and byte_a == last_byte_acc:
                break
            last_bit_acc = bit_a
            last_byte_acc = byte_a
            