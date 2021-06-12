import cv2
import numpy as np
from app.package.services import imbasic as imb
from app.package.services.mask import get_mask, get_circles


def process_circles(frame, circles):
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")

        for x, y, r in circles:
            frame = cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
            frame = cv2.rectangle(
                frame, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        return frame
    return frame


def process_frame(frame):
    # frame = cv2.flip(frame, 1)
    mask = get_mask(frame,
                    openSize=1,
                    closeSize=13)
    circles = get_circles(mask,
                          dp=3,
                          minDist=250)
    frame = process_circles(frame, circles)
    return frame, mask


def main():
    """Manual testing of the microphone detection system.
    """
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        frame, mask = process_frame(frame)

        imb.imshow(frame, width=550)
        imb.imshow(mask, width=550, win_name='mask')

        if cv2.waitKey(1) == ord('q'):
            break


if __name__ == '__main__':
    main()
