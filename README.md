# A customized MultiMMC implementation

Note: most of the core code is from the official implementation of [usnistgov/SP800-90B_EntropyAssessment](https://github.com/usnistgov/SP800-90B_EntropyAssessment). This repository is a customized version of the official implementation to support the following features:

- output the predictions
- calculate the accuracy using only part of the input data

## Usage

### Build the shared library

```bash
make
```

This will generate a shared library `libMultiMMC.so`.

### Install Python dependencies

```bash
pip install numpy
```

### Run the test

```bash
usage: multiMMC.py [-h] [-b] filename

MultiMMC Python Wrapper

positional arguments:
  filename

optional arguments:
  -h, --help       show this help message and exit
  -b, --bitstring  run input as bitstring
```