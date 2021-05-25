from app.package.services.grid import Grid
import numpy as np
import unittest


class TestGrid(unittest.TestCase):
    """ This is one of potentially many TestCases """

    def setUp(self):
        self.frame_size = np.array([400, 300])
        self.rows = [4, 3, 2, 1]
        self.cols = [1, 2, 3, 4]
        self.paddings = [10, 20, 30, 40]

        self.grids = []
        for i in range(len(self.rows)):
            self.grids.append(Grid(self.frame_size,
                                   self.rows[i],
                                   self.cols[i],
                                   self.paddings[i]))

    def test_locate_none_points(self):
        for grid in self.grids:
            points = [[0, 0],
                      [grid.padding, grid.padding],
                      [grid.size_of_frame[1]-grid.padding,
                          grid.size_of_frame[0]-grid.padding],
                      [grid.size_of_frame[1], grid.size_of_frame[0]]]
            results = np.array(
                [[0, 0],
                 [0, 0],
                 [grid.number_of_rows-1, grid.number_of_cols-1],
                 [grid.number_of_rows-1, grid.number_of_cols-1]])

            for index in range(len(points)):
                point = points[index]
                result = results[index]
                np.testing.assert_array_equal(
                    grid.locate_point(point),
                    result,
                    f'Error with point {point}' +
                    f'Should have been in grid: {result}')

    def test_points(self):
        """This may seem odd => point (60,20) correspond to the grid [1, 3]
        This is because the points are in the "Camera Space" (hor., vert.)
        And the Grid system uses [rows, cols] (the other way arround)
        """

        grid = Grid([100, 100], 5, 5, 0)
        points = [[60, 20], [40, 20], [40, 40], [0, 0]]
        results = [[1, 3], [1, 2], [2, 2], [0, 0]]
        results = np.array(results)

        for index in range(len(points)):
            point = points[index]
            result = results[index]
            actual = grid.locate_point(point)
            np.testing.assert_array_equal(
                actual,
                result,
                f'Error with point {point}\n' +
                f' w/ grid [{grid.number_of_rows},{grid.number_of_cols}]\n' +
                f' Result: {actual}\n' +
                f' Should have been in grid: {result}')

    def test_regions(self):
        tests = [{
            'grid': Grid([300, 100], 3, 1, 0),
            'regions': [(0, 0), (1, 0), (0, 1), (2, 0)],
            'results':  [
                [[0, 0], [100, 100]],
                [[0, 100], [100, 200]],
                None,
                [[0, 200], [100, 300]],
            ]
        }]

        for test in tests:
            grid = test['grid']
            regions = test['regions']
            results = test['results']
            # print(f' ** GRID SYSTEM: \n {grid}')

            for index, reg in enumerate(regions):
                _result = results[index]
                result = grid.get_region(reg)

                if (not result or not _result):
                    self.assertIsNone(result)
                    self.assertIsNone(_result)
                    continue

                np.testing.assert_array_almost_equal(result, _result)
                np.testing.assert_array_almost_equal(result, _result)


if __name__ == '__main__':
    unittest.main()
