#include <iostream>

#include "lemonator.h"
#include "hwlib.hpp"


lemonator hw  = lemonator.lemonator(2)
bool heater = False;

int empty_cup = 89;
int full_cup = 50;


void keep_temp(int d,int temp):

    float timer = 0;
    while(timer < d){
        timer += 0.8;
        hwlib::sleep(0.8);
        if (!heater && hw.temperature.read_mc() + 700 < temp - 500){
            heater = true;
            hw.heater.set(1)
        }
        else if (heater && hw.temperature.read_mc() + 700 > temp + 500){
            heater = false;
            hw.heater.set(0);
        }
    }
 

int calculate_sirup_level(float sirup_value, float water_value){
    return empty_cup - (empty_cup - full_cup) * (sirup_value / (sirup_value + water_value)) * sirup_value * 2;
}


void fill_cup(sirup_value, water_value){

    hw.sirup_pump.set(1);
    hw.sirup_valve.set(0);
    hw.water_pump.set(1);
    hw.water_valve.set(0);

    int sirup_level = calculate_sirup_level(sirup_value, water_value);

    while(hw.distance.read_mm() > sirup_level){
        keep_temp(0.2, 22000);
    }
    
    hw.sirup_pump.set(0);
    hw.sirup_valve.set(1);

    while(hw.distance.read_mm() > full_cup){
        keep_temp(0.2, 22000)
    }

    hw.water_pump.set(0);
    hw.water_valve.set(1);

    hw.heater.set(0);
    heater = true;
}

 
int main(int argc, char* argv[]){
    std::cout << "C++ Program Running" << std::endl;

        while(true){
            keypad_input = hw.keypad.getc()
            if(keypad_input == 'A'){
                fill_cup(1, 10)
            }
        
            if(keypad_input == 'B'){
                fill_cup(2, 10)
            }
        
            if(keypad_input == 'C'){
                fill_cup(1, 20)
            }
        
            if(keypad_input == 'D'){
                fill_cup(1, 3)
            }
        }

   
    
    return 0;
}



