import simulator_gui
import simulator

class output_dummy(object):
    def __init__(self, func):
        self.func = func

    def set(self, value):
        self.func(value)

class sensor_dummy(object):
    def __init__(self, func):
        self.func = func

    def get(self):
        return self.func()

    def getc(self):
        return self.func()

class lemonator(object):
    def __init__(self, port):
        self.port = port
        self.simulator = simulator.simulator()
        self.gui = simulator_gui.simulator_gui(self.simulator)

        self.led_yellow = output_dummy(self.gui.set_yellow_led)
        self.led_green = output_dummy(self.gui.set_green_led)

        self.heater = output_dummy(self.simulator.set_heater)
        self.sirup_pump = output_dummy(self.simulator.set_sirup)
        self.water_pump = output_dummy(self.simulator.set_water)
        self.sirup_valve = output_dummy(self.simulator.set_sirup_valve)
        self.water_valve = output_dummy(self.simulator.set_water_valve)

        self.keypad = sensor_dummy(self.gui.get_keypad)
        self.get = sensor_dummy(self.simulator.get_cup)
        self.read_mc = sensor_dummy(self.simulator.read_temp)
        self.read_mm = sensor_dummy(self.simulator.read_mm)
