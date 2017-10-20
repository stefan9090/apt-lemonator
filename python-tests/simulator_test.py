import simulator
import time
from unittest import *
import io
from contextlib import redirect_stdout

class simulator_test(TestCase):
    def test_heater(self):
        sim = simulator.simulator()
        current_time = 0
        last_time = time.time()

        original_temp = sim.read_real_temp()

        sim.set_heater(1)
        while not (current_time - last_time)>2:
            current_time = time.time()
            sim.update()

        value_before_cooling = sim.read_real_temp()

        sim.set_heater(0)
        while not (current_time - last_time)>5:
            current_time = time.time()
            sim.update()

        self.assertGreater(sim.read_real_temp(), original_temp, "Heater needs to heat if turned on")
        self.assertLess(sim.read_real_temp(), value_before_cooling, "Heater needs to cool if turned off")
        self.assertAlmostEqual(20085, sim.read_real_temp(), 1, "heater test failed")

    def test_sirup(self):
        sim = simulator.simulator()
        current_time = 0
        last_time = time.time()

        sim.set_sirup(1)
        sim.set_sirup_valve(0)
        while not (current_time - last_time) > 8:
            current_time = time.time()
            sim.update()

        sim.set_sirup(0)
        sim.set_sirup_valve(1)
        sim.update()

        self.assertAlmostEqual(85.8, sim.read_real_mm(), 1, "sirup test failed")

    def test_water(self):
        sim = simulator.simulator()
        current_time = 0
        last_time = time.time()

        sim.set_water(1)
        sim.set_water_valve(0)
        while not (current_time - last_time) > 8:
            current_time = time.time()
            sim.update()

        sim.set_water(0)
        sim.set_water_valve(1)
        sim.update()

        self.assertAlmostEqual(85.8, sim.read_real_mm(), 1, "water test failed")

    def test_valve_sirup(self):
        sim = simulator.simulator()
        current_time = 0
        last_time = time.time()

        sim.set_sirup(1)
        sim.set_sirup_valve(0)
        while not (current_time - last_time) > 8:
            current_time = time.time()
            sim.update()

        sim.set_sirup(0)
        sim.update()

        while not (current_time - last_time) > 30:
            current_time = time.time()
            sim.update()

        self.assertAlmostEqual(73.1, sim.read_real_mm(), 1, "sirup test failed")

    def test_valve_water(self):
        sim = simulator.simulator()
        current_time = 0
        last_time = time.time()

        sim.set_water(1)
        sim.set_water_valve(0)
        while not (current_time - last_time) > 8:
            current_time = time.time()
            sim.update()

        sim.set_water(0)
        sim.update()

        while not (current_time - last_time) > 30:
            current_time = time.time()
            sim.update()

        self.assertAlmostEqual(73.1, sim.read_real_mm(), 1, "water test failed")


    def test_read_mm(self):
        sim = simulator.simulator()
        current_time = 0
        last_time = time.time()

        is_equal = 0
        is_not_equal = 0

        sim.set_water(1)
        sim.set_water_valve(0)
        while not (current_time - last_time) > 4:
            current_time = time.time()
            sim.update()
            if sim.read_mm() == sim.read_real_mm():
                is_equal += 1
            else:
                is_not_equal += 1

        sim.set_water(0)
        sim.set_water_valve(1)
        sim.update()

        self.assertGreater(is_equal, 0, "need to have correct readings")
        self.assertGreater(is_not_equal, 0, "need to have incorrect readings")

    def test_temp_sensor_offset(self):
        sim = simulator.simulator()
        current_time = 0
        last_time = time.time()

        sim.set_heater(1)
        while not (current_time - last_time)>1.61:
            current_time = time.time()
            sim.update()
        sim.set_heater(0)
            
        self.assertAlmostEqual(sim.read_real_temp()-700, sim.read_temp(), 0, "read_temp returned wrong values")

    def test_cup_present(self):
        sim = simulator.simulator()
        sim.cup_present = False

        current_time = 0
        last_time = time.time()

        sim.set_heater(1)
        sim.water_pump_on()
        while not (current_time - last_time)>4:
            current_time = time.time()
            sim.update()
        sim.water_pump_off()
        sim.set_heater(0)

        self.assertEqual(sim.read_real_temp(), 20000, "heater turned on while no cup present")
        self.assertEqual(sim.liquid_level, 0, "pumps turned on while no cup present")

        sim.cup_present = True

        current_time = 0
        last_time = time.time()

        sim.water_pump_on()
        sim.set_heater(1)
        while not (current_time - last_time)>4:
            current_time = time.time()
            sim.update()
        sim.set_heater(0)
        sim.water_pump_off

        self.assertGreater(sim.read_real_temp(), 20000, "heater did not turn on while cup present")
        self.assertNotEqual(sim.liquid_level, 0, "pumps did not turn on while cup present")

    def test_set_cup(self):
        sim = simulator.simulator() 
        sim.set_cup(0)
        self.assertEqual(sim.get_cup(), False, "get_cup returned wrong value")

    def test_set_liquids_level(self):
        sim = simulator.simulator() 
        sim.set_liquids_level(10)
        self.assertEqual(sim.liquid_level, 10, "setting liquid level failed")

    def test_temp_sensor_lim(self):
        sim = simulator.simulator() 
        sim.temp_mc = 80000

        current_time = 0
        last_time = time.time()

        sim.set_heater(1)
        while not (current_time - last_time)>1:
            current_time = time.time()
            sim.update()
        
        self.assertEqual(sim.read_temp(), 70000, "read_temp returned wrong value")
        
simTester = simulator_test()
suite = TestLoader().loadTestsFromModule(simTester)
TextTestRunner().run(suite)
