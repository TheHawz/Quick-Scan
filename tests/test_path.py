from app.package.models.DisplayResultsModel import DisplayResultsModel
from app.package.services.path import interpolate_coords
from app.package.services.DspThread import DspThread
from app.package.services.grid import Grid
import numpy as np
import unittest

nan = np.nan


class TestGrid(unittest.TestCase):
    def setUp(self):
        pass

    def test_remove_nan(self):
        cases = [np.array([nan, nan, nan, 1, 1, 1, nan, nan, nan]),
                 np.array([1, 1, 1, nan, nan, nan]),
                 np.array([nan, nan, nan, 1, 1, 1])]

        results = [([1, 1, 1], 3, 3),
                   ([1, 1, 1], 0, 3),
                   ([1, 1, 1], 3, 0)]

        for index, case in enumerate(cases):
            result = interpolate_coords(case)
            # print(f' - Expected {results[index]} * Result -> {result}')
            np.testing.assert_almost_equal(result[0], results[index][0])
            self.assertEqual(result[1], results[index][1])
            self.assertEqual(result[2], results[index][2])

    def test_interpolate_coords(self):
        cases = [np.array([nan, nan, nan, 1, nan, 1, nan]),
                 np.array([nan, nan, -2, nan, nan, 2, nan, nan])]

        results = [([1, 1, 1], 3, 1),
                   ([-2, -2/3, 2/3,  2], 2, 2)]

        for index, case in enumerate(cases):
            result = interpolate_coords(case)
            # print(f' - Expected {results[index]} * Result -> {result}')
            np.testing.assert_almost_equal(result[0], results[index][0])
            self.assertEqual(result[1], results[index][1])
            self.assertEqual(result[2], results[index][2])

    def test_segmentation(self):
        worker = DspThread()
        model = DisplayResultsModel()

        # Starting on grid and moving inside grid
        model.data_x = [0, 10, 12,  15,
                        15, 15, 20, 20, 20, 13, 13, 13, 13]
        model.data_y = [0, 10,  12, 15,
                        15, 15, 20, 20, 20, 13, 13, 13, 13]
        model.grid = Grid([30, 30], 2, 3, 10)

        print(worker.segment_video(model))


if __name__ == '__main__':
    unittest.main()
