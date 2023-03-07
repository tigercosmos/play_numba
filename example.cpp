#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>

namespace py = pybind11;

extern "C" {

int add(int i, int j) { return i + j; }

py::array_t<double> array_add_value(const py::array_t<double>& in_arr, double v) {
  auto info = in_arr.request();
  double *out_buff = new double[info.size];
  auto in_ptr = (double *)info.ptr;
  for (py::ssize_t idx = 0; idx < info.size; ++idx) {
    *(out_buff + idx) = *(in_ptr + idx) + v;
  }
  auto out_info = py::buffer_info(out_buff, info.itemsize, info.format,
                                  info.ndim, info.shape, info.strides);
  return py::array_t<double>(out_info);
}

}

PYBIND11_MODULE(libexample, m) {
  m.doc() = "pybind11 example plugin";
  m.def("add", &add, "A function that adds two numbers");
  m.def("array_add_value", &array_add_value, "add value to array");
}
