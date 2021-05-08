from .package.services.grid import Grid, draw_grid
from .package.services.mask import get_mask, get_circles
from .package.services.path import interpolate_nan
from .package.services import colorSegmentation as cs
from .package.services import imbasic as imb
import numpy as np
import cv2
ximport os


# TODO: move to own file
TRACKING_COLOR = (220, 198, 43)  # BGR
BOTTOM_HSV_THRES = (80, 110, 10)
TOP_HSV_THRES = (130, 255, 255)

# TODO: move to own file
# GRID DEFINITION
NUMBER_OF_ROWS = 4
NUMBER_OF_COLS = 4
PADDING = 100


def main(file=None):
    cap = None

    if file is None:
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(file)

    size_of_frame = np.array([int(cap.get(3)), int(cap.get(4))])

    grid = Grid(size_of_frame, NUMBER_OF_ROWS, NUMBER_OF_COLS, PADDING)

    x_data = []
    y_data = []

    while cap.isOpened():
        success, frame = cap.read()
        # print(frame.shape)
        if not success:
            break

        frame = cv2.flip(frame, 1)

        mask = get_mask(frame)
        circles = get_circles(mask)

        frame = grid.draw_grid(frame)

        if circles is None:
            if len(x_data) != 0:
                x_data.append(np.nan)
                y_data.append(np.nan)
        else:
            x, y, r = np.round(circles[0, :]).astype("int")[0]
            x_data.append(x)
            y_data.append(y)
            frame = cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
            frame = cv2.rectangle(
                frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

        if len(x_data) != 0:
            grid_coords = grid.locate_point((x_data[-1], y_data[-1]))
            imb.draw_text(frame, f'{grid_coords[0], grid_coords[1]}', 15, 15)

        imb.imshow(frame, win_name="frame")
        imb.imshow(mask, win_name="mask")

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    cv2.destroyAllWindows()
    cap.release()

    # Interpolate missed frames
    if len(x_data) != 0 and len(y_data) != 0:
        x_data = interpolate_nan(x_data)
        y_data = interpolate_nan(y_data)

        if not os.path.exists('data'):
            os.makedirs('data')

        np.savetxt(os.path.join("data", "x_data.txt"), x_data)
        np.savetxt(os.path.join("data", "y_data.txt"), y_data)
        np.savetxt(os.path.join('data', 'size_of_frame.txt'), size_of_frame)


def audio_video_segmentation():
    """Esta función se encarga de recibir las listas de X_DATA & Y_DATA y de calcular
    los intervalos entre los que se ha detectado el micrófono en una región
    De esta forma si obtenemos: 
    regions = {
    ...,
    (28, 50): [1, 1],
    (51, 67): [0, 1],
    (68, 83): [0, 0], ...
    }

    Esto quiere decir que entre los frames 28 y 50 el microfono 
    se ha detectado en la región (1, 1). 
    entre los frames 51 y 67 en la region (0, 1).
    y entre los frames 68 y 83 en la region (0, 0).

    Con esta información podremos segmentar a posteriori el vector de audio.

    """
    size_of_frame = np.loadtxt(os.path.join('data', 'size_of_frame.txt'))
    x_data = np.loadtxt(os.path.join('data', 'x_data.txt'))
    y_data = np.loadtxt(os.path.join('data', 'y_data.txt'))

    data = np.transpose(np.array([x_data, y_data]))

    grid = Grid(size_of_frame, 2, 3, PADDING)
    grid_list = []
    for x, y in data:
        grid_id = grid.locate_point((x, y))
        grid_id = [int(i) for i in grid_id]  # np.array to python list
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

    cProfile.run('audio_video_segmentation()', 'output.dat')

    import pstats
    from pstats import SortKey

    with open("output_time.dat", "w") as f:
        p = pstats.Stats("output.dat", stream=f)
        p.sort_stats("time").print_stats()

    with open("output_calls.dat", "w") as f:
        p = pstats.Stats("output.dat", stream=f)
        p.sort_stats("calls").print_stats()
