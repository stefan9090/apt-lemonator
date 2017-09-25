#include "lemonator_dummy.hpp"

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#include "pybind11/pybind11.h"
#pragma GCC diagnostic pop

#include <stdio.h>
void test_func()
{
    printf("Test!!!!!!!!!!\n");
}

namespace py = pybind11;

PYBIND11_MODULE( lemonator, m ) {

   py::enum_< hwlib::buffering >( m, "buffering")
      .value( "unbuffered", hwlib::buffering::unbuffered )
      .value( "buffered", hwlib::buffering::buffered )
      .export_values();

   py::class_< output_dummy >( m, "output_dummy" )
      .def( "set", &output_dummy::set, "",
         py::arg("v"), py::arg("buffering") = hwlib::buffering::unbuffered );

   py::class_< lemonator_dummy >( m, "lemonator" )
      .def( py::init< int >() )
      .def_readonly( "led_yellow", &lemonator_dummy::d_led_yellow );

   m.def("test_func", &test_func);
}
