#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

extern "C"
{

  int add(int i, int j) { return i + j; }

  py::array_t<double> array_add_value(const py::array_t<double> &in_arr, double v)
  {
    auto info = in_arr.request();
    double *out_buff = new double[info.size];
    auto in_ptr = (double *)info.ptr;
    for (py::ssize_t idx = 0; idx < info.size; ++idx)
    {
      *(out_buff + idx) = *(in_ptr + idx) + v;
    }
    auto out_info = py::buffer_info(out_buff, info.itemsize, info.format,
                                    info.ndim, info.shape, info.strides);
    return py::array_t<double>(out_info);
  }

  py::array_t<double> create_array()
  {
    // Allocate and initialize some data; make this big so
    // we can see the impact on the process memory use:
    constexpr size_t size = 100 * 10 * 10;
    double *foo = new double[size];
    for (size_t i = 0; i < size; i++)
    {
      foo[i] = (double)i;
    }

    // Create a Python object that will free the allocated
    // memory when destroyed:
    py::capsule free_when_done(foo, [](void *f)
                               {
            double *foo = reinterpret_cast<double *>(f);
            delete[] foo; });

    return py::array_t<double>(
        {100, 10, 10},              // shape
        {10 * 10 * 8, 10 * 8, 8}, // C-style contiguous strides for double
        foo,                            // the data pointer
        free_when_done);                // numpy array references this parent
  }
}

PYBIND11_MODULE(libexample, m)
{
  m.doc() = "pybind11 example plugin";
  m.def("add", &add, "A function that adds two numbers");
  m.def("array_add_value", &array_add_value, "add value to array");
  m.def("create_array", &create_array, "create_array");
}
