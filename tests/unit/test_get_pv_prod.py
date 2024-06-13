import unittest

from pv_self_cons import get_pv_prod
from pv_self_cons import PvSystem, Shading


class TestGetPvProd(unittest.TestCase):

    def test_get_pv_prod(self):
        pvsystem = PvSystem(
            capacity=1.0,
            tilt=30,
            azimuth=180,
            shading=Shading(average=0.05),
            latitude=52.52,
            longitude=13.405,
        )
        get_pv_prod(pvsystem)


if __name__ == '__main__':
    unittest.main()
