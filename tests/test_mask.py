import os
import cv2
import numpy as np
import unittest

from app.package.services import imbasic as imb
from app.package.services.mask import get_mask, get_circles


class TestMask(unittest.TestCase):

    def setUp(self):
        paths = [os.path.join("tests", "imgs", "esfera1.jpg"),
                 os.path.join("tests", "imgs", "esfera2.jpg"),
                 ]
        self.imgs = []
        for path in paths:
            self.imgs.append(cv2.imread(path))

    def test_imgs(self):
        for index, img in enumerate(self.imgs):
            img = imb.resize(img, width=150)
            img = imb.resize(img, width=300)

            print(f'Shape: {img.shape}')
            mask = get_mask(img)
            circles = get_circles(mask)

            circles = np.round(circles[0, :]).astype("int")
            for x, y, r in circles:
                img = cv2.circle(img, (x, y), r, (0, 255, 0), 4)
                img = cv2.rectangle(
                    img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

            imb.imshow(img, win_name=f'Image {index}', width=400)
            cv2.waitKey(0)
            # print(circ)


if __name__ == '__main__':
    unittest.main()
