import os
import cv2
import numpy as np

from package.services import imbasic as imb
from package.services import colorSegmentation as cs
from package.services.path import interpolate_nan
from package.services.mask import improve_mask
from package.services.grid import Grid, draw_grid

# TODO: move to own file
TRACKING_COLOR = (220, 198, 43)  # BGR
BOTTOM_HSV_THRES = (80, 110, 10)
TOP_HSV_THRES = (130, 255, 255)

# TODO: move to own file
# GRID DEFINITION
NUMBER_OF_ROWS = 8
NUMBER_OF_COLS = 8
PADDING = 100


def main(file=None):
    cap = None

    if file is None:
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(file)

    width = cap.get(3)
    height = cap.get(4)
    size_of_frame = np.array([height, width])

    x_data = []
    y_data = []

    while cap.isOpened():
        success, frame = cap.read()
        # print(frame.shape)
        if not success:
            break

        mask = cs.getColorMask(frame, BOTTOM_HSV_THRES, TOP_HSV_THRES)
        mask = improve_mask(mask, cv2.MORPH_ELLIPSE, (7, 7))

        circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, dp=3, minDist=150)

        frame = draw_grid(frame, NUMBER_OF_ROWS, NUMBER_OF_COLS, PADDING)

        if circles is None:
            if len(x_data) != 0:
                x_data.append(np.nan)
                y_data.append(np.nan)
        else:
            circles = np.round(circles[0, :]).astype("int")

            for (x, y, r) in circles:
                frame = cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
                x_data.append(x)
                y_data.append(y)
                frame = cv2.rectangle(
                    frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                break

        imb.imshow(frame, win_name="frame")
        imb.imshow(mask, win_name="mask")

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()

    # Interpolate missed frames
    # if len(x_data) != 0 and len(y_data) != 0:
    #     x_data = interpolate_nan(x_data)
    #     y_data = interpolate_nan(y_data)
    #     np.savetxt(os.path.join("data", "x_data.txt"), x_data)
    #     np.savetxt(os.path.join("data", "y_data.txt"), y_data)
    #     np.savetxt(os.path.join('data', 'size_of_frame.txt'), size_of_frame)


def audio_video_segmentation():
    size_of_frame = np.loadtxt(os.path.join('data', 'size_of_frame.txt'))
    x_data = np.loadtxt(os.path.join('data', 'x_data.txt'))
    y_data = np.loadtxt(os.path.join('data', 'y_data.txt'))

    data = np.transpose(np.array([x_data, y_data]))

    grid = Grid(size_of_frame, 2, 3, PADDING)
    grid_list = []
    for x, y in data:
        grid_id = grid.locate_point((x, y))
        grid_id = [int(i) for i in grid_id]
        grid_list.append(grid_id)

    start = 0
    end = 0
    grid = grid_list[0]

    dictionary = {}

    for index in range(len(grid_list)):
        _grid = grid_list[index]

        if grid == _grid:
            end = index
        else:
            dictionary[(start, end)] = _grid
            start = index
            end = index
            grid = _grid

    print(dictionary)


if __name__ == "__main__":
    import cProfile

    cProfile.run('main()', 'output.dat')

    import pstats
    from pstats import SortKey

    with open("output_time.dat", "w") as f:
        p = pstats.Stats("output.dat", stream=f)
        p.sort_stats("time").print_stats()

    with open("output_calls.dat", "w") as f:
        p = pstats.Stats("output.dat", stream=f)
        p.sort_stats("calls").print_stats()
