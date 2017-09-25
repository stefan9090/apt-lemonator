cmake_minimum_required(VERSION 2.8.12)
project(cmake_example)

include_directories("RS-232/")
include_directories("hwlib/library/")
include_directories("vkatp-lemonator/library/")

set(LIBRARY_SOURCES
    RS-232/rs232.c
    hwlib/library/hwlib.cpp)

add_subdirectory(pybind11)
pybind11_add_module(python_interface python-interface/main.cpp ${LIBRARY_SOURCES})
