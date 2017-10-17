#include <iostream>
#include <string>

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#include "pybind11/embed.h"
#include "pybind11/pybind11.h"
#pragma GCC diagnostic pop

#include "lemonator_interface.hpp"

namespace py = pybind11;

//py::object distance = lemonator_obj.attr("distance");
//py::object temperature = lemonator_obj.attr("temperature");
//py::object keypad = lemonator_obj.attr("keypad");
//py::object heater = lemonator_obj.attr("heater");
//py::object reflex = lemonator_obj.attr("get");

//py::object py_output_dummy = lemonator.attr("output_dummy");
//py::object py_sensor_dummy = lemonator.attr("sensor_dummy");

class output_simulator : public hwlib::pin_out{
private:
    py::object output_obj;
public:
    output_simulator(py::object & lemonator_obj, std::string output):
        output_obj(lemonator_obj.attr(output.c_str()))
    {}
    
    void set(bool b, hwlib::buffering buf = hwlib::buffering::unbuffered){
        output_obj.attr("set")(b);
    }
};

class sensor_simulator : 
    public hwlib::sensor_temperature, 
    public hwlib::sensor_distance, 
    public hwlib::sensor_rgb,
    public hwlib::istream,
    public hwlib::pin_in
{
private:
    py::object sensor_obj;
    
public:
    sensor_simulator(py::object & lemonator_obj, std::string sensor):
        sensor_obj(lemonator_obj.attr(sensor.c_str()))
    {}
    
    int read_mc()override{
        return py::int_(sensor_obj.attr("read_mc")());
    }
    int read_mm()override{
        return py::int_(sensor_obj.attr("read_mm")());
    }
    rgb read_rgb()override{
        /*
          py::object py_rgb = py_sensor_dummy.attr("read_rgb")();
          return rgb(
          py::int_(py_rgb.attr(u8"r")),
          py::int_(py_rgb.attr(u8"g")),
          py::int_(py_rgb.attr(u8"b"))
          );
        */
    }
    char getc()override{
        return py::int_(sensor_obj.attr("getc")());
    }
    bool get(
        hwlib::buffering buf = hwlib::buffering::unbuffered    
        )override{  
        return py::bool_(sensor_obj.attr("get")());
    }
};

class filler_simulator {
public:
    output_simulator & pump;
    output_simulator & valve;	
    filler_simulator(output_simulator & pump, output_simulator & valve):
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
    py::object lemonator_obj;
    lcd_dummy        lcd;
    
    sensor_simulator keypad;
    sensor_simulator distance;
    sensor_simulator color;
    sensor_simulator temperature;
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

    lemonator_simulator(py::object & lemonator_obj):
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
        keypad(lemonator_obj, "keypad"),
        distance(lemonator_obj, "distance"),
        color(lemonator_obj, "color"),
        temperature(lemonator_obj, "temperature"),
        reflex(lemonator_obj, "reflex"),

        heater(lemonator_obj, "heater"),
        sirup_pump(lemonator_obj, "sirup_pump"),
        sirup_valve(lemonator_obj, "sirup_valve"),
        water_pump(lemonator_obj, "water_pump"),
        water_valve(lemonator_obj, "water_valve"),
        led_green(lemonator_obj, "led_green"),
        led_yellow(lemonator_obj, "led_yellow"),
        sirup(sirup_pump, sirup_valve),
        water(water_pump, water_valve)
    {}   
};
