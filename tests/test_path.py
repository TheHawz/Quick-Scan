from app.package.services.path import interpolate_coords
import numpy as np
import unittest

nan = np.nan


class TestGrid(unittest.TestCase):
    """ This is one of potentially many TestCases """

    def setUp(self):
        pass

    def test_nan_removal(self):
        cases = [np.array([nan, nan, nan, 1, 1, 1, nan, nan, nan]),
                 np.array([1, 1, 1, nan, nan, nan])]

        results = [([1, 1, 1], 3, 3),
                   ([1, 1, 1], 0, 3)]

        for index, case in enumerate(cases):
            result = interpolate_coords(case)
            np.testing.assert_array_equal(result[0], results[index][0])
            self.assertEqual(result[1], results[index][1])
            self.assertEqual(result[2], results[index][2])


if __name__ == '__main__':
    unittest.main()
