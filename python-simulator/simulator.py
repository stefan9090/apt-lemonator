import time
import math
import lemonator
import time
from unittest import *
import io
from random import randint

"""
the simulator class simulats the values the would be given by the hardware
the simulator class will do this as close to the real hardware a posible.
"""
class simulator:

    #initialize the variables for the simulator
    def __init__(self):
        self.last_time = time.time()
        self.sirup_pump_time = 0
        self.water_pump_time = 0

        self.heater_state = False
        self.temp_mc = 20000
        self.delayed_temp_mc = 0
        self.target_temp = 30000
        self.temp_delay_ms = 0.8
        self.temp_delay_timer = 0

        self.liquid_level = 0
        self.mix_vessel_height_cm = 5
        self.mix_vessel_radius_cm = 5
        self.mix_vessel_max_level = math.pi * (self.mix_vessel_radius_cm**2) * self.mix_vessel_height_cm
        self.height_sensor_cm = 8.9

        self.sirup_pump_state = False
        self.sirup_pump_running = False
        self.water_pump_state = False
        self.water_pump_running = False
        self.sirup_valve_state = False
        self.water_valve_state = False
        self.sirup_rampdown = False
        self.water_rampdown = False

        self.cup_present = True

        self.multiplier = 5
        
    #get the current cup_present value false if not pressent true otherwise
    def get_cup(self):
        return self.cup_present
        
    #set whether the cup_present is pressent or not    
    def set_cup(self,value):
        return self.cup_present
        
    #set te current liquid_level in the cup
    def set_liquids_level(self, value):
        self.liquid_level = 0
        
    #turns the heater on or of depending on the bool value given    
    def set_heater(self, value):
        self.heater_state = value
        
    #turns the sirup pump on only if the cup is pressent and pump not on already
    def sirup_pump_on(self):
        if self.cup_present == True and not self.sirup_pump_state:
            self.sirup_pump_time = time.time()
            self.sirup_pump_state = True

    #turns the sirup pump off        
    def sirup_pump_off(self):
        self.sirup_pump_time = time.time()
        self.sirup_pump_state = False
        
    #turns the sirup pump on or of depending on the bool value given    
    def set_sirup(self, value):
        if value:
            self.sirup_pump_on()
        else:
            self.sirup_pump_off()
    
    #turns the sirup pump valve on or of depending on the bool value given
    def set_sirup_valve(self, value):
        self.sirup_pump_time = time.time()
        self.sirup_valve_state = value
    
    #turns the water pump on only if the cup is pressent and pump not on already
    def water_pump_on(self):
        if self.cup_present == True and not self.water_pump_state:
            self.water_pump_time = time.time()
            self.water_pump_state = True
    
    #turns water pump off
    def water_pump_off(self):
        self.water_pump_time = time.time()
        self.water_pump_state = False

    #turns the water pump on or of depending on the bool value given
    def set_water(self, value):
        if value:
            self.water_pump_on()
        else:
            self.water_pump_off()

    #turns the water pump valve on or of depending on the bool value given
    def set_water_valve(self, value):
        self.water_pump_time = time.time()
        self.water_valve_state = value
    
    #returns the last cashed value of the heater only updates ones every 800ms
    def read_temp(self):
        if self.delayed_temp_mc>70000:
            return 70000 - 700 #sensor offset
        return self.delayed_temp_mc - 700 #sensor offset

    #the actual temp value the function ignores the 800ms read out delay
    def read_real_temp(self):
        return self.temp_mc
    
    #simulates the temperature if heater on temp up temp down if heater off
    def handle_temperature(self, dt):
        if self.heater_state == False and self.temp_mc>20000:
            self.temp_mc -= 1 * self.multiplier * dt
        elif self.heater_state == True and self.temp_mc<100000:
            self.temp_mc += 10 * self.multiplier * dt
            
    #simulates the height sensor includes the random miss read values
    def read_mm(self):
        mm = (self.height_sensor_cm - self.liquid_level / (math.pi * self.mix_vessel_radius_cm**2))*10
        if randint(0, 9) == 1:
            mm += randint(5, 30)
        return mm
        
    #returns the accurate value of the height sensor 
    def read_real_mm(self):
        mm = (self.height_sensor_cm - self.liquid_level / (math.pi * self.mix_vessel_radius_cm**2))*10
        return mm
        
    #simulates the liquid pumps
    def handle_liquids(self, dt):
        sirup_stream = 0
        if self.sirup_pump_state == True and self.sirup_valve_state == False:
            if (time.time() - self.sirup_pump_time)>3:
                sirup_stream = 1 * self.multiplier * dt
                self.sirup_pump_running = True
        elif self.sirup_pump_state == False and self.sirup_pump_running == True:
            if self.sirup_valve_state == True:
                sirup_stream = 0
                self.sirup_pump_running = False
            else:
                if (time.time() - self.sirup_pump_time)>20:
                    sirup_stream = 0
                    self.sirup_pump_running = False
                else:
                    sirup_stream = 1 * self.multiplier * dt
        else:
            if self.sirup_pump_running:
                sirup_stream = 0
                self.sirup_pump_running = False


        water_stream = 0
        if self.water_pump_state == True and self.water_valve_state == False:
            if (time.time() - self.water_pump_time)>3:
                water_stream = 1 * self.multiplier * dt
                self.water_pump_running = True
        elif self.water_pump_state == False and self.water_pump_running == True:
            if self.water_valve_state == True:
                water_stream = 0
                self.water_pump_running = False
            else:
                if (time.time() - self.water_pump_time)>20:
                    water_stream = 0
                    self.water_pump_running = False
                else:
                    water_stream = 1 * self.multiplier * dt
        else:
            if self.water_pump_running:
                water_stream = 0
                self.water_pump_running = False

        self.liquid_level += sirup_stream + water_stream

    #gives clear debug values 
    def log(self):
        print("\n====Log====")
        print("liquid_level in ml: %5f" % (self.liquid_level,))
        print("distance to liquid in mm: %5f" % (self.read_mm(),))
        print("liquid in mix vessel in mm: %5f" % (100 - self.read_mm(),))
        print("sensor temperature in mc: %5f" % (self.read_temp(),))
        print("real temperature in mc: %5f" % (self.read_real_temp(),))
        print("water: pump = " + str(self.water_pump_state) + ", valve = " + str(self.water_valve_state))
        print("sirup: pump = " + str(self.sirup_pump_state) + ", valve = " + str(self.sirup_valve_state))

    #update all sensors call when update needed
    def update(self):
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        self.handle_temperature(dt)
        self.handle_liquids(dt)
        if (current_time - self.temp_delay_timer) > self.temp_delay_ms:
            self.delayed_temp_mc = self.temp_mc
            self.temp_delay_timer = current_time
            
#only for debug purpuse 
if __name__=="__main__":
    sim = simulator()

    delay_time = 0.013
    last_time = time.time()

    sim.sirup_pump_on()
    sim.water_pump_on()
    sim.heater_on()

    while(True):
        sim.update()
        current_time = time.time()
        #if(current_time - last_time)>1:
        sim.log()
        #    last_time = current_time
        time.sleep(0.1)
