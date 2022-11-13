from asyncio.windows_events import NULL
import cv2
import numpy as np


class Face():
    def __init__(self, tipeMakeUp = 'lips'):
        self.tipeMakeUp = tipeMakeUp
        self.hitung1 = 0
        self.hitung2 = 0
        self.tambah = 0
        
    
    def getPoints(self, pointAwal, pointAkhir, points):
        self.pointAwal = pointAwal
        self.pointAkhir = pointAkhir
        self.point = points[self.pointAwal:self.pointAkhir]

    
    def setPoint(self, point1, point2) :
        self.hitung1 = point1[0][0]    
        self.hitung2 = point2[0][0]
        
        self.tambah = (self.hitung2 - self.hitung1) * 0.15
        self.hitung1 += self.tambah
        self.hitung2 -= self.tambah

    def createBoxLips(self, img, points, scale=5, masked=False, cropped=True, tipe='lips'):
        if masked:
            mask = np.zeros_like(img)
            if tipe == 'pipi' :
                mask = cv2.polylines(mask, [points], True, (255, 255, 255), 80)
                # mask = cv2.circle(mask, points[1], 10, (255, 255, 255), 30)
            else :
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
        kernel = np.ones((5,5),np.float32)/100
        self.color = cv2.filter2D(self.color,-1,kernel)
        self.color = cv2.GaussianBlur(self.color, (7, 7), 10)
        self.color = cv2.addWeighted(oriImage, 1, self.color, 0.4, 0)
        