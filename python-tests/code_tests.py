import lemonator
import time
from unittest import *
import io
from contextlib import redirect_stdout

from main import *


class lemonator_code_test(TestCase):
    def test_sirup_level(self):
        self.assertAlmostEqual(81.9, calculate_sirup_level(1, 10), 1, "sirup level test failed")
        self.assertAlmostEqual(76, calculate_sirup_level(1, 5), 1, "sirup level test failed")
        self.assertAlmostEqual(69.5, calculate_sirup_level(1, 3), 1, "sirup level test failed")
        self.assertAlmostEqual(85.3, calculate_sirup_level(1, 20), 1, "sirup level test failed")
        self.assertAlmostEqual(65, calculate_sirup_level(4, 9), 1, "sirup level test failed")

sdt = lemonator_code_test()
suite = TestLoader().loadTestsFromModule(sdt)
TextTestRunner().run(suite)
