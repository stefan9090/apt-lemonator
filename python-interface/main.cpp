#include "lemonator_dummy.hpp"
#include "tcs3200.hpp"

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#include "pybind11/pybind11.h"
#pragma GCC diagnostic pop

#include <stdio.h>

namespace py = pybind11;

PYBIND11_MODULE( lemonator, m ) {

   py::enum_< hwlib::buffering >( m, "buffering")
      .value( "unbuffered", hwlib::buffering::unbuffered )
      .value( "buffered", hwlib::buffering::buffered )
      .export_values();

   py::class_< output_dummy >( m, "output_dummy" )
      .def( "set", &output_dummy::set, "",
         py::arg("v"), py::arg("buffering") = hwlib::buffering::unbuffered );

   py::class_<sensor_dummy>(m, "sensor_dummy")
       .def("read_mc", &sensor_dummy::read_mc)
       .def("read_mm", &sensor_dummy::read_mm)
       .def("read_rgb", &sensor_dummy::read_rgb)
       .def("getc", &sensor_dummy::getc)
       .def("get", &sensor_dummy::get, py::arg("buf") = hwlib::buffering::unbuffered);

   py::class_<lcd_dummy>(m, "lcd_dummy")
       .def("putc", &lcd_dummy::putc);

   //py::class_<hwlib::sensor_rgb>(m, "sensor_rgb");
   
   py::class_<hwlib::sensor_rgb::rgb>(m, "rgb")
       .def(py::init<int, int, int>())
       .def_readwrite("r", &hwlib::sensor_rgb::rgb::r)
       .def_readwrite("g", &hwlib::sensor_rgb::rgb::g)
       .def_readwrite("b", &hwlib::sensor_rgb::rgb::b);
       
   py::class_< lemonator_dummy >( m, "lemonator" )
       .def( py::init< int >() )
       .def_readonly("lcd", &lemonator_dummy::d_lcd)
       .def_readonly("keypad", &lemonator_dummy::d_keypad)
       .def_readonly("distance", &lemonator_dummy::d_distance)
       .def_readonly("color", &lemonator_dummy::d_color)
       .def_readonly("temperature", &lemonator_dummy::d_temperature)
       .def_readonly("reflex", &lemonator_dummy::d_reflex)
       .def_readonly("heater", &lemonator_dummy::d_heater)
       .def_readonly("sirup_pump", &lemonator_dummy::d_sirup_pump)
       .def_readonly("sirup_valve", &lemonator_dummy::d_sirup_valve)
       .def_readonly("water_pump", &lemonator_dummy::d_water_pump)
	   .def_readonly("water_valve", &lemonator_dummy::d_water_valve)
       .def_readonly("led_yellow", &lemonator_dummy::d_led_yellow)
       .def_readonly("led_green", &lemonator_dummy::d_led_green);
}
