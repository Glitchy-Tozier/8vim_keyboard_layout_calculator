from cffi import FFI
ffibuilder = FFI()

with open('cffi_extension.h') as f:
    header = f.read()

ffibuilder.cdef(header)

ffibuilder.set_source("_cffi_extension",  # name of the output C extension
"""
    #include "cffi_extension.h"
""",
    sources=['cffi_extension.c'],
    libraries=[])

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
