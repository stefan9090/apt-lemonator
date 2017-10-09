import simulator
import time
from unittest import *
import io
from contextlib import redirect_stdout

class simulator_test(TestCase):
    def test_heater(self):
        print('testing heater')
        sim = simulator.simulator()
        sim.set_heater(1)
        current_time = 0
        last_time = time.time()
        while not (current_time - last_time)>2:
            current_time = time.time()
            sim.update()
        sim.set_heater(0)
        while not (current_time - last_time)>1:
            current_time = time.time()
            sim.update()
        self.assertAlmostEqual(20100, sim.read_real_temp(), 1, "heater test failed")
        
        
simTester = simulator_test()
suite = TestLoader().loadTestsFromModule(simTester)
TextTestRunner().run(suite) 
