# A customized MultiMMC implementation

Note: most of the core code is from the official implementation of [usnistgov/SP800-90B_EntropyAssessment](https://github.com/usnistgov/SP800-90B_EntropyAssessment). This repository is a customized version of the official implementation to support the following features:

- output the predictions
- calculate the accuracy using only part of the input data
- print accuracies in a format that is compatible with my plotting script
- support multiple files as input
- use `d` = [8, 16, 32, 64, 96] instead of only 16 (as in official implementation)

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
usage: multiMMC.py [-h] -f FILES [FILES ...] [-u] [-d DATASET] [-c COLOR]

MultiMMC Python Wrapper

optional arguments:
  -h, --help            show this help message and exit
  -f FILES [FILES ...], --files FILES [FILES ...]
                        files to test
  -u, --human           human readable
  -d DATASET, --dataset DATASET
                        override dataset name
  -c COLOR, --color COLOR
                        override color name
```

## NIST License notice

The original NIST License notice is provided below:

>NIST-developed software is provided by NIST as a public service. You may use, copy, and distribute copies of the software in any medium, provided that you keep intact this entire notice. You may improve, modify, and create derivative works of the software or any portion of the software, and you may copy and distribute such modifications or works. Modified works should carry a notice stating that you changed the software and should note the date and nature of any such change. Please explicitly acknowledge the National Institute of Standards and Technology as the source of the software.
>
>NIST-developed software is expressly provided "AS IS." NIST MAKES NO WARRANTY OF ANY KIND, EXPRESS, IMPLIED, IN FACT, OR ARISING BY OPERATION OF LAW, INCLUDING, WITHOUT LIMITATION, THE IMPLIED WARRANTY OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, NON-INFRINGEMENT, AND DATA ACCURACY. NIST NEITHER REPRESENTS NOR WARRANTS THAT THE OPERATION OF THE SOFTWARE WILL BE UNINTERRUPTED OR ERROR-FREE, OR THAT ANY DEFECTS WILL BE CORRECTED. NIST DOES NOT WARRANT OR MAKE ANY REPRESENTATIONS REGARDING THE USE OF THE SOFTWARE OR THE RESULTS THEREOF, INCLUDING BUT NOT LIMITED TO THE CORRECTNESS, ACCURACY, RELIABILITY, OR USEFULNESS OF THE SOFTWARE.
>
>You are solely responsible for determining the appropriateness of using and distributing the software and you assume all risks associated with its use, including but not limited to the risks and costs of program errors, compliance with applicable laws, damage to or loss of data, programs or equipment, and the unavailability or interruption of operation. This software is not intended to be used in any situation where a failure could cause risk of injury or damage to property. The software developed by NIST employees is not subject to copyright protection within the United States.
