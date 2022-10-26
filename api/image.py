import cv2
import numpy as np


class Face:
    def __init__(self, pointAwal, pointAkhir, points):
        self.pointAwal = pointAwal
        self.pointAkhir = pointAkhir
        self.point = points[pointAwal:pointAkhir]

    def createBoxLips(self, img, points, scale=5, masked=False, cropped=True):
        if masked:
            mask = np.zeros_like(img)
            mask = cv2.fillPoly(mask, [points], (255, 255, 255))

        if cropped:
            bbox = cv2.boundingRect(points)
            x, y, w, h = bbox
            imgCrop = img[y:y + h, x:x + w]
            imgCrop = cv2.resize(imgCrop, (0, 0), None, scale, scale)
            return imgCrop

        else:
            return mask

    def masking(self, oriImage, b, g, r):
        self.color = np.zeros_like(self.image)
        self.color[:] = b, g, r
        self.color = cv2.bitwise_and(self.image, self.color)
        self.color = cv2.GaussianBlur(self.color, (7, 7), 10)
        self.color = cv2.addWeighted(oriImage, 1, self.color, 0.4, 0)
        