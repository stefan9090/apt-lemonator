#include <iostream>

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#include "pybind11/pybind11.h"
#pragma GCC diagnostic pop

#include "lemonator_interface.hpp"

namespace py = pybind11;

py::object lemonator = py::module::import(u8"lemonator");
py::object py_output_dummy = lemonator.attr(u8"output_dummy");
py::object py_sensor_dummy = lemonator.attr(u8"sensor_dummy");

class output_simulator : public hwlib::pin_out{
public:
    void set(bool b, hwlib::buffering buf = hwlib::buffering::unbuffered){
        py_output_dummy.attr(u8"set")(b);
    }
};

class sensor_simulator : 
   public hwlib::sensor_temperature, 
   public hwlib::sensor_distance, 
   public hwlib::sensor_rgb,
   public hwlib::istream,
   public hwlib::pin_in
{
public:
   int read_mc()override{
       return py::int_(py_sensor_dummy.attr(u8"read_mc")());
   }
   int read_mm()override{
       return py::int_(py_sensor_dummy.attr(u8"read_mm")());
   }
   rgb read_rgb()override{
       py::object py_rgb = py_sensor_dummy.attr(u8"read_rgb")();
       return rgb(
           py::int_(py_rgb.attr(u8"r")),
           py::int_(py_rgb.attr(u8"g")),
           py::int_(py_rgb.attr(u8"b"))
       );
   }
   char getc()override{
       return py::int_(py_sensor_dummy.attr(u8"getc")());
   }
   bool get(
      hwlib::buffering buf = hwlib::buffering::unbuffered    
   )override{  
       return py::bool_(py_sensor_dummy.attr(u8"get")());
   }
};

class filler_simulator {
public:
   output_simulator & pump;
   output_simulator & valve;	
   filler_simulator(
      output_simulator & pump,
      output_simulator & valve
   ):
      pump(pump), 
      valve(valve)
   {}	  
};

class lcd_dummy : public hwlib::ostream {	
public:   
   void putc( char c ){
       std::cout<<"c";
   }
};

class lemonator_simulator : public lemonator_interface{
public:
    lcd_dummy        lcd;
    
    sensor_simulator keypad;
    sensor_simulator distance;
    sensor_simulator color;
    sensor_simulator temperature;
    sensor_simulator presence;
    sensor_simulator reflex;
   
    output_simulator heater;
    output_simulator sirup_pump;
    output_simulator sirup_valve;
    output_simulator water_pump;
    output_simulator water_valve;
    output_simulator led_green;
    output_simulator led_yellow;

    filler_simulator sirup;
    filler_simulator water;

    lemonator_simulator():
      lemonator_interface(
          lcd,
          keypad,
          distance,
          color,
          temperature,
          reflex,
          heater,
          sirup_pump,
          sirup_valve,
          water_pump,
          water_valve,
          led_green,
          led_yellow	  
	  ),
      lcd(),
      keypad(),
      distance(),
      color(),
      temperature(),
      reflex(),
      heater(),
      sirup_pump(),
      sirup_valve(),
      water_pump(),
      water_valve(),
      led_green(),
      led_yellow(),

      sirup(sirup_pump, sirup_valve),
      water(water_pump, water_valve)
   {}	  
};
