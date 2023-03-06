import sysconfig
from pathlib import Path

import numpy as np
from llvmlite import binding
from numba import jit
from numba.core import types, typing


@jit(nopython=True)  # Set "nopython" mode for best performance, equivalent to @njit
def go_fast(a):  # Function is compiled to machine code when called the first time
    trace = 0.0
    for i in range(a.shape[0]):  # Numba likes loops
        trace += np.tanh(a[i, i])  # Numba likes NumPy functions
    return a + trace  # Numba likes NumPy broadcasting


# load the library into LLVM
lib_path = Path(f"libexample{sysconfig.get_config_var('EXT_SUFFIX')}")
if not lib_path.exists():
    raise ValueError(f"extension lib not found: {lib_path}")
binding.load_library_permanently(str(lib_path.absolute()))

# Adds typing information
c_func = types.ExternalFunction(
    "add", typing.signature(types.int64, types.int64, types.int64)
)


@jit(nopython=True)
def _example(x: int, y: int):
    return c_func(x, y)


def example(x: int, y: int):
    if not isinstance(x, int):
        x = int(x)
    if not isinstance(y, int):
        y = int(y)
    return _example(x, y)


if __name__ == "__main__":
    print(go_fast(np.arange(100).reshape(10, 10)))
    print(example(3, 4))
