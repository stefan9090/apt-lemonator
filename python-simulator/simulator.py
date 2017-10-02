import time

class simulator:
    def __init__(self):
        self.last_time = time.time()
        self.sirup_pump_time = 0
        self.water_pump_time = 0

        self.heater_state = False
        self.temp = 20
        self.target_temp = 30

        self.liquid_level = 0

        self.sirup_pump_state = False
        self.sirup_pump_running = False
        self.water_pump_state = False
        self.water_pump_running = False
        self.water_valve_state = False
        self.sirup_valve_state = False

        self.cup_present = True

    def heater_on(self):
        self.heater_state = True

    def heater_off(self):
        self.heater_state = False

    def set_heater(self, value):
        self.heater_state = value

    def sirup_pump_on(self):
        if self.cup_present == True:
            self.sirup_pump_time = time.time()
            self.sirup_pump_state = True

    def sirup_pump_off(self):
        self.sirup_pump_time = time.time()
        self.sirup_pump_state = False

    def set_sirup(self, value):
        if value:
            self.sirup_pump_on()
        else:
            self.sirup_pump_off()

    def water_pump_on(self):
        if self.cup_present == True:
            self.water_pump_time = time.time()
            self.water_pump_state = True

    def water_pump_off(self):
        self.water_pump_time = time.time()
        self.water_pump_state = False

    def set_water(self, value):
        if value:
            self.water_pump_on()
        else:
            self.water_pump_off()

    def read_temp(self):
        if self.temp>70:
            return 70
        return self.temp

    def handle_heater(self, dt):
        if self.heater_state == False and self.temp>21:
            self.temp -= 1 * dt
        elif self.heater_state == True and self.temp<100:
            self.temp += 2 * dt

    def handle_liquids(self, dt):
        sirup_stream = 0
        if self.sirup_pump_state == True:
            if (time.time() - self.sirup_pump_time)>3:
                sirup_stream = 1 * dt
                self.sirup_pump_running = True
        else:
            if self.sirup_pump_state == False and self.sirup_pump_running == True:
                if (time.time() - self.sirup_pump_time)>20:
                    sirup_stream = 0
                    self.sirup_pump_running = False
                else:
                    sirup_stream = 1 * dt

        water_stream = 0
        if self.water_pump_state == True:
            if (time.time() - self.water_pump_time)>3:
                water_stream = 1 * dt
                self.water_pump_running = True
        else:
            if self.water_pump_state == False and self.water_pump_running == True:
                if (time.time() - self.water_pump_time)>20:
                    water_stream = 0
                    self.water_pump_running = False
                else:
                    water_stream = 1 * dt

        self.liquid_level += sirup_stream + water_stream


    def update(self):
        current_time = time.time()
        dt = current_time - self.last_time
        self.last_time = current_time
        self.handle_heater(dt)
        self.handle_liquids(dt)

if __name__=="__main__":
    sim = simumlator_interface(lemon)

    sim.heater_on()

    delay_time = 0.013
    last_time = time.time()

    sim.sirup_pump_on()
    sim.water_pump_on()

    val = True

    while(True):
        sim.update()
        print("%5f" % (sim.liquid_level,))
        current_time = time.time()
        if(current_time - last_time)>10 and val:
            val = False
            print('Going False!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
            sim.sirup_pump_off()
        time.sleep(0.1)
