import random
import numpy as np
import cv2
from app.package.services.imbasic import imshow


def show_rect(color):
    color = np.array(color, dtype=np.uint8)
    frame = np.ones((200, 200, 3), dtype=np.uint8) * color

    frame = frame.astype(np.uint8)

    imshow(frame, win_name=str(color), width=350)
    cv2.waitKey(0)


def create_color_map(color0=(255, 0, 0), color1=(0, 0, 255)):
    LUT = np.linspace(color0, color1, 100)
    return LUT


def test(spl=[]):
    spl = np.linspace(140, 143, 50)

    lut = create_color_map()

    min = np.min(spl)
    max = np.max(spl)

    for _ in range(10):
        value = spl[random.randint(0, len(spl)-1)]
        print(value)
        index = int((value-min)*len(lut) / (max-min)) - 1
        print(index)
        show_rect(lut[index-1])

    # 143-140 -> 100
    #   x-140 -> y


if __name__ == '__main__':
    test()
