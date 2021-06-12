import cv2
import numpy as np
from time import time
from app.package.services import imbasic as imb


def main(device=2, use_dshow=False):
    device_dshow = device+cv2.CAP_DSHOW
    cap = cv2.VideoCapture((device, device_dshow)[use_dshow])

    ret, _ = cap.read()
    if not ret:
        raise Exception('Driver error!')

    expected_fps = cap.get(cv2.CAP_PROP_FPS)
    if not use_dshow:
        print(f'Expected FSP: {expected_fps}')
    else:
        print(f'Expected FPS (with DSHOW) {expected_fps}')

    times = []

    while True:
        if len(times) > 300:
            break

        t1 = time()
        ret, frame = cap.read()
        times.append(time()-t1)

        if not ret:
            break

        imb.imshow(frame)
        key = cv2.waitKey(1)

        if key == ord('q'):
            break

    cv2.destroyAllWindows()
    return times[3:]


def inverse(x):
    if x != 0:
        return 1/x
    else:
        return 0


def a():
    times = main()

    fps = np.array(list(map(inverse, times)))
    print(' - Media: ', np.median(fps))
    print(' - STD : ', np.std(fps))
    print(' - min : ', np.max(fps))
    print(' - max : ', np.min(fps))

    import matplotlib.pyplot as plt

    # matplotlib histogram
    plt.hist(fps, color='blue', edgecolor='black',
             bins=10)

    # Add labels
    plt.xlabel('FPS')
    plt.show()


if __name__ == '__main__':
    a()
