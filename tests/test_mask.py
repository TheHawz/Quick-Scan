import os
import cv2
import numpy as np
import unittest

from app.package.services import imbasic as imb
from app.package.services.mask import get_mask, get_circles


class TestMask(unittest.TestCase):

    def setUp(self):
        paths = [os.path.join("tests", "imgs", "esfera 1.jpg"),
                 os.path.join("tests", "imgs", "esfera 2.jpg"),
                 ]
        self.imgs = []
        for path in paths:
            self.imgs.append(cv2.imread(path))

    def test_imgs(self):
        for index, img in enumerate(self.imgs):
            img_small, sf = imb.resize(
                img, width=250, return_scale_factor=True)
            print(sf)

            mask = get_mask(img_small)
            circles = get_circles(mask)

            circles = np.round(circles[0, :]).astype("int")
            for x, y, r in circles:
                x = int(x/sf)
                y = int(y/sf)
                r = int(r/sf)

                img = cv2.circle(img, (x, y), r, (0, 255, 0), 4)
                img = cv2.rectangle(
                    img, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)

            imb.imshow(img, win_name=f'Image {index}', width=400)
            cv2.imwrite(os.path.join('tests', 'imgs',
                        'result_'+str(index)+'.png'), img)
            cv2.waitKey(0)
            # print(circ)


if __name__ == '__main__':
    unittest.main()
