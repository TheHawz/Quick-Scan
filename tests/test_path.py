from app.package.models.DisplayResultsModel import DisplayResultsModel
from app.package.services.path import interpolate_coords
from app.package.services.DspThread import DspThread
from app.package.services.grid import Grid
import numpy as np
import unittest

import matplotlib.pyplot as plt

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

    def plot_grid(self, model):
        p = model.grid.padding
        s = model.grid.size_of_frame

        for h in model.grid.hor_div:
            plt.plot([0+p, s[1]-p], [h, h], 'k')
        for v in model.grid.ver_div:
            plt.plot([v, v], [0+p, s[0]-p], 'k')

    def test_segmentation(self):
        worker = DspThread()
        model = DisplayResultsModel()

        # Starting on grid and moving inside grid
        model.grid = Grid([50, 40], 4, 3, 5)
        model.data_x = [6, 7, 6]
        model.data_x.extend([8, 6])
        model.data_x.extend([6, 6, 6])
        model.data_x.extend([9, 9, 9, 9])
        model.data_y = [6, 6, 8]
        model.data_y.extend([28, 28])
        model.data_y.extend([23, 22, 21])
        model.data_y.extend([6, 6, 8, 12])

        model.data_x = (np.array(model.data_x)*2).tolist()
        model.data_y = (np.array(model.data_y)*2).tolist()

        self.plot_grid(model)
        plt.plot(model.data_x, model.data_y, 'o-')
        plt.xlim((0, model.grid.size_of_frame[1]))
        plt.ylim((0, model.grid.size_of_frame[0]))
        plt.xlabel('Horizontal')
        plt.ylabel('Vertical')

        print(worker.segment_video(model))

        # plt.gca().invert_xaxis()
        plt.gca().invert_yaxis()
        plt.show()


if __name__ == '__main__':
    unittest.main()
