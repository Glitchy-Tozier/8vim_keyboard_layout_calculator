# CFFI extension for faster execution times

The _8vim keyboard layout calculator_ calculates the scores of millions of layouts which takes time (around 13 minutes on a laptop with the default configuration using PyPy). When you try different configurations, you spend a lot of time waiting.

For faster execution times, the two "bottleneck" functions `testSingleLayout` and `getTopScores` have been rewritten in C. See the article [Speed up Python with CFFI](https://maximilian-schillinger.de/articles/speed-up-python-with-cffi.html) for how these function were determined as bottlenecks.

This "C extension" can be used in `main.py` thanks to [CFFI](https://cffi.readthedocs.io/en/latest/), the _C Foreign Function Interface for Python_. If you use the _PyPy_ interpreter, _cffi_ should be already installed. Otherwise it can be installed via `pip install cffi`. See [Installation and Status](https://cffi.readthedocs.io/en/latest/installation.html) for details.

If you want to use the C extension, you need to enable it in the configuration file `config.py`: Set `USE_CFFI` to `True`.

And you need to compile the extension. This can be done with:

```sh
cd cffi
pypy3 cffi_extension_build.py
cd ..
```

This will use a C compiler in the background. If you don't have one installed, install one and try again.

If you want to use _CPython_ (the default Python interpreter), run `python3 cffi_extension_build.py` instead. It's important to use the same Python interpreter for compiling the C extension and running the calculator! This step is only necessary once (except when you change the C code in this folder).

Then run the calculator as usual with:

```sh
pypy3 main.py
```

or

```sh
python3 main.py
```
