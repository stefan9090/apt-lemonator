import simulator_gui
import simulator

class output_dummy(object):
    def __init__(self, func, simulator, gui):
        self.func = func
        self.simulator = simulator
        self.gui = gui

    def set(self, value):
        self.func(value)

class sensor_dummy(object):
    def __init__(self, func, simulator, gui):
        self.func = func
        self.simulator = simulator
        self.gui = gui

    def get(self):
        return self.func()

    def getc(self):
        return self.func()

class lemonator(object):
    def __init__(self, port):
        self.port = port
        self.simulator = simulator.simulator()
        self.gui = simulator_gui.simulator_gui(self.simulator)

        self.led_yellow = output_dummy(self.gui.set_yellow_led, self.simulator, self.gui)
        self.led_green = output_dummy(self.gui.set_green_led, self.simulator, self.gui)

        self.heater = output_dummy(self.simulator.set_heater, self.simulator, self.gui)
        self.sirup_pump = output_dummy(self.simulator.set_sirup, self.simulator, self.gui)
        self.water_pump = output_dummy(self.simulator.set_water, self.simulator, self.gui)
        self.sirup_valve = output_dummy(self.simulator.set_sirup_valve, self.simulator, self.gui)
        self.water_valve = output_dummy(self.simulator.set_water_valve, self.simulator, self.gui)

        self.keypad = sensor_dummy(self.gui.get_keypad, self.simulator, self.gui)
