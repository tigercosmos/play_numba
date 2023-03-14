import numba
import sysconfig
from pathlib import Path
import numpy as np
from llvmlite import binding
from numba import jit
from numba.core import types, typing
import libexample
import logging

# ===========================================================================

# Numba know the type

print(numba.typeof(libexample.create_array()))

# ===========================================================================

# load the library into LLVM
lib_path = Path(f"libexample{sysconfig.get_config_var('EXT_SUFFIX')}")
if not lib_path.exists():
    raise ValueError(f"extension lib not found: {lib_path}")
binding.load_library_permanently(str(lib_path.absolute()))

c_create_array = types.ExternalFunction(
    "create_array",
    typing.signature(
        types.Array(types.float64, 3, "C"),
    ),
)

@jit(nopython=True)
def create_array():
    return c_create_array()

if __name__ == "__main__":
    create_array()
