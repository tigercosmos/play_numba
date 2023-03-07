import sysconfig
from pathlib import Path

import numpy as np
from llvmlite import binding
from numba import jit
from numba.core import types, typing
from libexample import array_add_value as pybind_array_add_value


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

c_array_func = types.ExternalFunction(
    "array_add_value",
    typing.signature(
        types.Array(types.float64, 2, "C"),
        types.Array(types.float64, 2, "C", readonly=True),
        types.float64,
    ),
)


@jit(nopython=True)
def _example(x: int, y: int):
    return c_func(x, y)


@jit(nopython=True)
def array_add_value(in_arr: np.ndarray, v: float):
    return c_array_func(in_arr, v)


def example(x: int, y: int):
    if not isinstance(x, int):
        x = int(x)
    if not isinstance(y, int):
        y = int(y)
    return _example(x, y)


if __name__ == "__main__":
    print(go_fast(np.arange(100).reshape(10, 10)))
    print(example(3, 4))
    x = np.random.rand(10, 10).astype(np.float64)
    out = array_add_value(x, 3.0)
    out_pybind = pybind_array_add_value(x, 3.0)
    print(out)
    print(np.allclose(out, out_pybind))
