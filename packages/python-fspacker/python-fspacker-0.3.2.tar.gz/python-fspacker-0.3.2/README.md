[![Python package](https://github.com/FusionSolutions/python-fspacker/actions/workflows/python-package.yml/badge.svg)](https://github.com/FusionSolutions/python-fspacker/actions/workflows/python-package.yml)
# Fusion Solutions message packer

## Introduction

Message packer for socket communications.
Pure-Python implementation and it is [*slightly slower*](#benchmark) as `pickle`, `marshal` or even `json`, but much safer for production.
The following types are supported for packing and unpacking:
 - `None`
 - Booleans: `True` and `False`
 - `int`
 - Floats: `float`, `inf` and `-inf`
 - `str`
 - `bytearray` (during unpacking it will be converted to `bytes`)
 - `bytes`
 - `list` (during unpacking it will be converted to `tuple`)
 - `tuple`
 - `dict` (dict key type can be any from this list)
 - `set`

## Installation

Requires python version 3.8 or later.

To install the latest release on [PyPI](https://pypi.org/project/python-fspacker/),
simply run:

```shell
pip3 install python-fspacker
```

Or to install the latest version, run:

```shell
git clone https://github.com/FusionSolutions/python-fspacker.git
cd python-fspacker
python3 setup.py install
```

## Python library

### Usage

Use like `pickle` with `dump`, `dumps`, `load` and `loads` functions.

```python
import fsPacker

data = fsPacker.dumps(["test"]*5)
print( fsPacker.loads(data) )
```

### Benchmark

Environment: Intel(R) Xeon(R) CPU E5-1650 v4 @ 3.60GHz, DIMM DDR4 Synchronous Registered (Buffered) 2133 MHz
```shell
$/python-fspacker: python3 -m benchmark
Batch 1# started
  pickle
    packed data size:    369436 byte
    dump : best: 0.00097681 <- median avg: 0.00097981 - average: 0.00098675 -> worst: 0.00115466
    loads: best: 0.00116250 <- median avg: 0.00116567 - average: 0.00116768 -> worst: 0.00123618
  marshal
    packed data size:    474624 byte
    dump : best: 0.00060849 <- median avg: 0.00060978 - average: 0.00061214 -> worst: 0.00066010
    loads: best: 0.00093875 <- median avg: 0.00094239 - average: 0.00094469 -> worst: 0.00099110
  FSPacker version 1
    packed data size:    348332 byte
    dump : best: 0.00140599 <- median avg: 0.00142470 - average: 0.00143550 -> worst: 0.00179069
    loads: best: 0.00092720 <- median avg: 0.00108024 - average: 0.00107529 -> worst: 0.00113729
  FSPacker PURE PYTHON version 1
    packed data size:    329293 byte
    dump : best: 0.02668814 <- median avg: 0.02687568 - average: 0.02691436 -> worst: 0.02727839
    loads: best: 0.02563514 <- median avg: 0.02585654 - average: 0.02623195 -> worst: 0.02991657
  FSPacker version 2
    packed data size:    324346 byte
    dump : best: 0.00133745 <- median avg: 0.00135156 - average: 0.00136461 -> worst: 0.00155367
    loads: best: 0.00094138 <- median avg: 0.00107694 - average: 0.00107477 -> worst: 0.00114164
  FSPacker PURE PYTHON version 2
    packed data size:    314318 byte
    dump : best: 0.02291694 <- median avg: 0.02304409 - average: 0.02304181 -> worst: 0.02318106
    loads: best: 0.02749131 <- median avg: 0.02768044 - average: 0.02768100 -> worst: 0.02799873

Batch 2# started
  pickle
    packed data size:    274491 byte
    dump : best: 0.00084737 <- median avg: 0.00085283 - average: 0.00085566 -> worst: 0.00091460
    loads: best: 0.00100438 <- median avg: 0.00101581 - average: 0.00101901 -> worst: 0.00110241
  marshal
    packed data size:    360242 byte
    dump : best: 0.00051488 <- median avg: 0.00051733 - average: 0.00051980 -> worst: 0.00054507
    loads: best: 0.00083179 <- median avg: 0.00083660 - average: 0.00084212 -> worst: 0.00090665
  FSPacker version 1
    packed data size:    271694 byte
    dump : best: 0.00146050 <- median avg: 0.00147431 - average: 0.00147690 -> worst: 0.00153197
    loads: best: 0.00092286 <- median avg: 0.00100156 - average: 0.00099671 -> worst: 0.00102327
  FSPacker PURE PYTHON version 1
    packed data size:    238499 byte
    dump : best: 0.02538159 <- median avg: 0.02551851 - average: 0.02557210 -> worst: 0.02591332
    loads: best: 0.02445310 <- median avg: 0.02459201 - average: 0.02464271 -> worst: 0.02524533
  FSPacker version 2
    packed data size:    238735 byte
    dump : best: 0.00135346 <- median avg: 0.00136909 - average: 0.00137037 -> worst: 0.00141406
    loads: best: 0.00090187 <- median avg: 0.00100334 - average: 0.00101569 -> worst: 0.00130636
  FSPacker PURE PYTHON version 2
    packed data size:    221546 byte
    dump : best: 0.02124800 <- median avg: 0.02136108 - average: 0.02141090 -> worst: 0.02174148
    loads: best: 0.02539373 <- median avg: 0.02556542 - average: 0.02576320 -> worst: 0.02921140

Batch 3# started
  pickle
    packed data size:    274511 byte
    dump : best: 0.00087786 <- median avg: 0.00088081 - average: 0.00088287 -> worst: 0.00093917
    loads: best: 0.00098829 <- median avg: 0.00099558 - average: 0.00099822 -> worst: 0.00105612
  marshal
    packed data size:    360267 byte
    dump : best: 0.00051608 <- median avg: 0.00051854 - average: 0.00051974 -> worst: 0.00054176
    loads: best: 0.00082532 <- median avg: 0.00082907 - average: 0.00083079 -> worst: 0.00085855
  FSPacker version 1
    packed data size:    414729 byte
    dump : best: 0.00300953 <- median avg: 0.00304670 - average: 0.00307232 -> worst: 0.00353145
    loads: best: 0.00209713 <- median avg: 0.00237827 - average: 0.00240026 -> worst: 0.00317319
  FSPacker PURE PYTHON version 1
    packed data size:    365886 byte
    dump : best: 0.06813255 <- median avg: 0.06852698 - average: 0.06859602 -> worst: 0.06918136
    loads: best: 0.06472549 <- median avg: 0.06544865 - average: 0.06549210 -> worst: 0.06638827
  FSPacker version 2
    packed data size:    381787 byte
    dump : best: 0.00308844 <- median avg: 0.00310415 - average: 0.00311051 -> worst: 0.00318295
    loads: best: 0.00206454 <- median avg: 0.00235557 - average: 0.00234600 -> worst: 0.00239830
  FSPacker PURE PYTHON version 2
    packed data size:    348954 byte
    dump : best: 0.06123471 <- median avg: 0.06176491 - average: 0.06173875 -> worst: 0.06195223
    loads: best: 0.07077837 <- median avg: 0.07135906 - average: 0.07146089 -> worst: 0.07298397

Batch 4# started
  pickle
    packed data size:        97 byte
    dump : best: 0.00055353 <- median avg: 0.00056210 - average: 0.00056276 -> worst: 0.00057487
    loads: best: 0.00064643 <- median avg: 0.00065715 - average: 0.00065725 -> worst: 0.00066493
  marshal
    packed data size:        79 byte
    dump : best: 0.00047902 <- median avg: 0.00048745 - average: 0.00048688 -> worst: 0.00049302
    loads: best: 0.00058795 <- median avg: 0.00059175 - average: 0.00059234 -> worst: 0.00060103
  FSPacker version 1
    packed data size:        85 byte
    dump : best: 0.00077319 <- median avg: 0.00078550 - average: 0.00078805 -> worst: 0.00080470
    loads: best: 0.00068854 <- median avg: 0.00076246 - average: 0.00075894 -> worst: 0.00078787
  FSPacker PURE PYTHON version 1
    packed data size:        85 byte
    dump : best: 0.01360374 <- median avg: 0.01369004 - average: 0.01373398 -> worst: 0.01407292
    loads: best: 0.01672420 <- median avg: 0.01689699 - average: 0.01688315 -> worst: 0.01702459
  FSPacker version 2
    packed data size:        74 byte
    dump : best: 0.00075289 <- median avg: 0.00076416 - average: 0.00076328 -> worst: 0.00077514
    loads: best: 0.00053710 <- median avg: 0.00055360 - average: 0.00055652 -> worst: 0.00058802
  FSPacker PURE PYTHON version 2
    packed data size:        74 byte
    dump : best: 0.00831298 <- median avg: 0.00834915 - average: 0.00835809 -> worst: 0.00851608
    loads: best: 0.01466914 <- median avg: 0.01474124 - average: 0.01477603 -> worst: 0.01507150
```
## Contribution

Bug reports, constructive criticism and suggestions are welcome. If you have some create an issue on [github](https://github.com/FusionSolutions/python-fspacker/issues).

## Copyright

All of the code in this distribution is Copyright (c) 2021 Fusion Solutions Kft.

The utility is made available under the GNU General Public license. The included LICENSE file describes this in detail.

## Warranty

THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. THE ENTIRE RISK AS TO THE USE OF THIS SOFTWARE IS WITH YOU.

IN NO EVENT WILL ANY COPYRIGHT HOLDER, OR ANY OTHER PARTY WHO MAY MODIFY AND/OR REDISTRIBUTE THE LIBRARY, BE LIABLE TO YOU FOR ANY DAMAGES, EVEN IF SUCH HOLDER OR OTHER PARTY HAS BEEN ADVISED OF THE POSSIBILITY OF SUCH DAMAGES.

Again, see the included LICENSE file for specific legal details.