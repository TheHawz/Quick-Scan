import cv2
import os
from app.package.services import imbasic as imb


def save_frame(img, fname):
    path = os.path.join('tests', 'img_acq', 'imgs')
    if not os.path.exists(path):
        os.mkdir(path)
    cv2.imwrite(os.path.join(path, fname), img)


def main():
    """Manual testing of the microphone detection system.
    """
    cap = cv2.VideoCapture(1)

    i = 0
    while True:
        ret, frame = cap.read()

        imb.imshow(frame, width=550)

        if i > 0 and i % 10 == 0:
            save_frame(frame, fname=str(i)+'.png')

        if cv2.waitKey(1) == ord('q'):
            break

        i += 1


if __name__ == '__main__':
    main()
