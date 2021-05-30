import numpy as np
import unittest


from app.package.services.DspThread import DspThread
from app.package.services.grid import Grid
from app.package.models.DisplayResultsModel import DisplayResultsModel


class TestSpatialSegmentation(unittest.TestCase):
    """ This is one of potentially many TestCases """

    def log(self, d: dict) -> None:
        for key in [*d]:
            print(f'[{key}]: {d[key]}')

    def setUp(self):
        self.frame_size = np.array([6])
        self.rows = 2
        self.cols = 2
        self.paddings = 0

        self.grid: Grid = Grid(self.frame_size, self.rows, self.cols, 0)
        print(self.grid.hor_div)
        print(self.grid.ver_div)

    def test_without_padding(self):
        data_x = [0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]
        data_y = [0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4]

        model = DisplayResultsModel()
        worker = DspThread()
        model.data_x = data_x
        model.data_y = data_y
        model.grid = self.grid

        d = worker.segment_video(model)
        # self.log(d)


if __name__ == '__main__':
    unittest.main()
