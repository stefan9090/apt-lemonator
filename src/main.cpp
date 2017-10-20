#include <iostream>

#include "lemonator_proxy.hpp"
#include "hwlib.hpp"

#include <chrono>
#include <thread>

#include "main.hpp"

#define simulator
#ifdef simulator

#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#include "pybind11/embed.h"
#include "pybind11/pybind11.h"
#pragma GCC diagnostic pop
#include "../cpp-interface/simulator-interface.hpp"

#endif //simulator

#ifndef simulator
#define lemonator lemonator_proxy
#else
#define lemonator lemonator_simulator
#endif

static bool heater = false;

static int empty_cup = 89;
static int full_cup = 50;

namespace hwlib {
void wait_ms(int delay) {
    std::this_thread::sleep_for(std::chrono::milliseconds(delay));
}
}


void keep_temp(lemonator& hw, int d,int temp) {

    float timer = 0;
    while(timer < d){
        timer += 0.8;
        hwlib::wait_ms(800);
        if (!heater && hw.temperature.read_mc() + 700 < temp - 500){
            heater = true;
            hw.heater.set(1);
        }
        else if (heater && hw.temperature.read_mc() + 700 > temp + 500){
            heater = false;
            hw.heater.set(0);
        }
    }
}

int calculate_sirup_level(float sirup_value, float water_value){
    return empty_cup - (empty_cup - full_cup) * (1 / (sirup_value + water_value)) * sirup_value * 2;
}


void fill_cup(lemonator& hw, int sirup_value, int water_value){

    hw.sirup_pump.set(1);
    hw.sirup_valve.set(0);
    hw.water_pump.set(1);
    hw.water_valve.set(0);

    int sirup_level = calculate_sirup_level(sirup_value, water_value);

    while(hw.distance.read_mm() > sirup_level){
        keep_temp(hw, 0.2, 22000);
    }

    hw.sirup_pump.set(0);
    hw.sirup_valve.set(1);

    while(hw.distance.read_mm() > full_cup){
        keep_temp(hw, 0.2, 22000);
    }

    hw.water_pump.set(0);
    hw.water_valve.set(1);

    hw.heater.set(0);
    heater = true;
}

#ifndef testing
int main(int argc, char* argv[]){
    std::cout << "C++ Program Running" << std::endl;

#ifndef simulator
    lemonator_proxy hw = lemonator_proxy(24, 1, 0);
#else
    Py_Initialize();
    wchar_t wstr[32];
    wchar_t* args = {wstr};
    std::mbstowcs(wstr, "lemonator", 9);
    PySys_SetArgv(1, &args);

    lemonator_simulator hw = lemonator_simulator(24);
#endif
    hwlib::wait_ms(3000);

    while(true){
        char keypad_input = hw.keypad.getc();

        std::cout << keypad_input << std::endl;

        if(keypad_input == 'A'){
            fill_cup(hw, 1, 10);
        }

        if(keypad_input == 'B'){
            fill_cup(hw, 2, 10);
        }

        if(keypad_input == 'C'){
            fill_cup(hw, 1, 20);
        }

        if(keypad_input == 'D'){
            fill_cup(hw, 1, 3);
        }
    }

    Py_Finalize();

    return 0;
}
#endif //testing
