# CFFI extension for faster execution times

The _8vim keyboard layout calculator_ calculates the scores of millions of layouts which takes time (around 13 minutes on a laptop with the default configuration using PyPy). When you try different configurations, you spend a lot of time waiting.

For faster execution times, the two "bottleneck" functions `testSingleLayout` and `getTopScores` have been rewritten in C. See the article [Speed up Python with CFFI](https://maximilian-schillinger.de/articles/speed-up-python-with-cffi.html) for how these function were determined as bottlenecks.

This "C extension" can be used in `main.py` thanks to [CFFI](https://cffi.readthedocs.io/en/latest/), the _C Foreign Function Interface for Python_. If you use the _PyPy_ interpreter, _cffi_ should be already installed. Otherwise it can be installed via `pip install cffi`. See [Installation and Status](https://cffi.readthedocs.io/en/latest/installation.html) for details.

If you want to use the C extension, you need to enable it in the configuration file `config.py`: Set `USE_CFFI` to `True`.

## Usage

| 1. Decide on Interpreter         | pypy3<br>(recommended)                                 | python3                                                  |
|:---------------------------------|--------------------------------------------------------|----------------------------------------------------------|
| 2. Install package (Linux only?) | pypy3-dev                                              | python3-dev                                              |
| 3. Get `cffi`                    | Included by default                                    | Run `pip install cffi`                                   |
| 4. Build code                    | Run `cd cffi && pypy3 cffi_extension_build.py ; cd ..` | Run `cd cffi && python3 cffi_extension_build.py ; cd ..` |
| 5. Start optimizer               | Run `pypy3 main.py`                                    | Run `python3 main.py`                                    |

Remarks:

* Step 2: If there is no `pypy3-dev` (or `python3-dev`) package for your distribution (p.e. Arch Linux), just install `pypy3` (or `python`).
* Step 4 will use a C compiler in the background. If you don't have one installed, install one (p.e. `gcc`, `clang` or `tcc`) and try again.
