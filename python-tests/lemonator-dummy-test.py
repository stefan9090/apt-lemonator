import lemonator
import time
from unittest import *
import io
from contextlib import redirect_stdout

print( "Python interface demo running" )
hw = lemonator.lemonator( 2 )


class lemonator_dummy_test(TestCase):
    def setUp(self):
        self.lemon = lemonator.lemonator(2)
        self.out = io.StringIO()

    def test_keypad(self):
        self.assertEqual('D', self.lemon.keypad.getc(), "keypad test failed")

    def test_distance(self):
        self.assertEqual(42, self.lemon.distance.read_mm(), "distance test failed")

    def test_temperature(self):
        self.assertEqual(370, self.lemon.temperature.read_mc(), "temparature test failed")

    def test_reflex(self):
        self.assertEqual(1, self.lemon.reflex.get(), "reflex test failed")

    def test_rgb(self):
        rgb = self.lemon.color.read_rgb()
        r = rgb.r
        g = rgb.g
        b = rgb.b
        self.assertEqual(12, r, "color test for r value failed")
        self.assertEqual(13, g, "color test for g value failed")
        self.assertEqual(14, b, "color test for b value failed")
        
sdt = lemonator_dummy_test()
suite = TestLoader().loadTestsFromModule(sdt)
TextTestRunner().run(suite) 
