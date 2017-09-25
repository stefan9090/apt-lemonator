cmake_minimum_required(VERSION 2.8.12)
project(lemonator)

include_directories("RS-232/")
include_directories("hwlib/library/")
include_directories("vkatp-lemonator/library/")

set(LIBRARY_SOURCES
    RS-232/rs232.c
    hwlib/library/hwlib.cpp)

set(CMAKE_C_FLAGS "-fdata-sections -ffunction-sections -DBMPTK_TARGET_native")
set(CMAKE_CXX_FLAGS "-fdata-sections -ffunction-sections -DBMPTK_TARGET_native")

add_subdirectory(pybind11)
pybind11_add_module(lemonator python-interface/main.cpp ${LIBRARY_SOURCES})
