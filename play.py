import os

import numpy as np
from llvmlite import binding
from numba import jit
from numba.core import types, typing
import sysconfig

x = np.arange(100).reshape(10, 10)


@jit(nopython=True)  # Set "nopython" mode for best performance, equivalent to @njit
def go_fast(a):  # Function is compiled to machine code when called the first time
    trace = 0.0
    for i in range(a.shape[0]):  # Numba likes loops
        trace += np.tanh(a[i, i])  # Numba likes NumPy functions
    return a + trace  # Numba likes NumPy broadcasting


print(go_fast(x))

# load the library into LLVM
path = os.path.abspath(f"libexample{sysconfig.get_config_var('EXT_SUFFIX')}")
binding.load_library_permanently(path)

# Adds typing information
c_func = types.ExternalFunction(
    "add", typing.signature(types.int64, types.int64, types.int64)
)


@jit(nopython=True)
def example(x, y):
    return c_func(x, y)


print(example(3, 4))
