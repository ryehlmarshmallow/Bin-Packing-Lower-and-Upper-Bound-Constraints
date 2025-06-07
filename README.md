# Bin Packing with Lower and Upper Bound Constraints

## Introduction

The Bin packing Lower and Upper Bound Constraints is a variant of the Multi Knapsacks Problem (MKP) where the objective is to pack a subset of the items into a fixed number of bins, with varying capacities, so that the total value of the packed items is a maximum. In this problem, each bin also has a lower bound capacity, while the objective is still the same. This project presents various optimization methods, along with analyzing the performance of these approaches to find the best method for the problem.

## Table of Contents

- [Introduction](#introduction)
- [Description](#description)
- [Installation](#installation)
- [Folder Structure](#folder-structure)
- [Usage](#usage)
- [Hardware Specifications](#hardware-specifications)

## Description

The project implements several optimization methods to solve the Bin Packing Lower and Upper Bound Constraints problem, including:
- Constraint Programming (CP)
- Integer Programming (IP)
- Greedy Algorithm (G)
- Genetic Algorithm (GA)
- Tabu Search (TS)
- Local Search (LS)
- Dynamic Programming (DP)

The methods are implemented in both Python and C++, with the Greedy and Genetic Algorithm implemented in C++ for better performance. The project also includes a benchmarking script to evaluate the performance of these methods on various test cases.

## Installation

Linux is recommended for running this project, as we encountered the deadlock issue of the Python `subprocess` library on Windows, as mentioned in [the 'subprocess' documentation](https://docs.python.org/3/library/subprocess.html#subprocess.Popen.poll):

> This will deadlock when using `stdout=PIPE` or `stderr=PIPE` and the child process generates enough output to a pipe such that it blocks waiting for the OS pipe buffer to accept more data. Use `Popen.communicate()` when using pipes to avoid that.

Clone the repository:

```bash
git clone https://github.com/ryehlmarshmallow/Bin-Packing-Lower-and-Upper-Bound-Constraints.git
cd Bin-Packing-Lower-and-Upper-Bound-Constraints
```

Install the prerequisites:

- Python: 3.11 or higher

```bash
pip install -r requirements.txt
```

- C++: GCC compiler, C++17 or higher

## Folder Structure

```
.
├── checker.py
├── dist
│   ├── cp.py
│   ├── dp.py
│   ├── g
│   ├── ga
│   ├── ip.py
│   ├── ls.py
│   └── ts.py
├── makefile
├── README.md
├── requirements.txt
├── scripts
├── src
│   ├── cpp
│   │   ├── ga.cpp
│   │   └── g.cpp
│   └── py
│       ├── cp.py
│       ├── dp.py
│       ├── ip.py
│       ├── ls.py
│       └── ts.py
└── test
    └── 40 test cases...
```

## Usage

The `src` folder contains the source code for the optimization methods, with Greedy and Genetic Algorithm implemented in C++, while the rest are in Python.

To run the optimization methods, first make sure you have the required dependencies installed, then execute the following command:

```bash
make all
```


This will compile the C++ codes and put the executables in the `dist` folder, along with the Python scripts. If you want to modify the code, you can edit the files in the `src/cpp` and `src/py` folders, and then run the `make all` command again to recompile the C++ code.

Then, you can run the optimization methods with the following command:

```bash
python scripts/checker.py --time-limit 10 -r
```

This command will run all the optimization methods with a time limit of 10 seconds. You can adjust the time limit by changing the `--time-limit` parameter, and remove the `-r` flag to not remove the previous benchmark results.

The benchmark results will be saved in the `output` folder, with `data.pkl` containing the `pandas.DataFrame` format, and `data.tex` containing the LaTeX table format.

## Hardware Specifications

The benchmarks were run on a machine with the following specifications:

- **CPU**: AMD Ryzen 7 7735HS, 8 cores, 16 threads, 3.2 GHz base clock, 4.75 GHz boost clock, 16 MB L3 cache
- **RAM**: 16 GB DDR5, 4800 MT/s, dual-channel
- **OS**: Arch Linux, kernel 6.14.9-arch1-1.1-g14
- **Power Management**: Performance mode enabled, no overclocking.

## Benchmark Details

The Constraint Programming and Integer Programming methods were run using the `ortools` library, while the Greedy and Genetic Algorithm methods were implemented in C++ for performance reasons. The Tabu Search, Local Search, and Dynamic Programming methods were implemented in Python.

The Constraint Programming method is multi-threaded, while the rest is single-threaded. The benchmarks were run on various test cases, including both small and large instances of the Bin Packing Lower and Upper Bound Constraints problem, as well as edge cases to test the performance of the methods.

## Acknowledgements

- Deepest gratitude to advisor Ph.D. Dung Q. Pham for guidance and support throughout the project.
- Appreciation to Minh T. Dinh, Khoi H. Nguyen, and Hieu T. Pham for their contributions and collaboration.
- Thanks to the open-source community for providing libraries and tools that made this project possible.