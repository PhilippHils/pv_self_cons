import unittest

from pv_self_cons import get_consumption
from pv_self_cons import Consumer


class TestGetConsumption(unittest.TestCase):

    def test_get_consumption(self):
        consumer = Consumer(profile="H0", annual_consumption=1000)
        consumption = get_consumption(consumer)
        self.assertAlmostEqual(consumption.sum(), 1000, delta=1)


if __name__ == '__main__':
    unittest.main()
