from api.imageDetector import ImageDetector
from api.face import Face

import cv2
import numpy as np


class Proses():
    def __init__(self, warna, tipeMakeUp, request, *args, **kwargs):
        self.imageDetector = ImageDetector(request, *args, **kwargs)
        self.face = Face(tipeMakeUp)
        self.r = warna[0]
        self.g = warna[1]
        self.b = warna[2]
        
        # start image filter
        for face in self.imageDetector.faces:
            landmarks = self.imageDetector.predictor(self.imageDetector.gray_image, face)
            my_points = []
            for n in range(68):
                # if n <= 9 :
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                my_points.append([x, y])

            my_points = np.array(my_points)
            
            if tipeMakeUp == 'lips' :
                self.face.getPoints(48, 61, my_points)
                self.face.image = self.face.createBoxLips(self.imageDetector.image, self.face.point, 2, masked=True, cropped=False, tipe=tipeMakeUp)
                self.face.masking(self.imageDetector.original_image, self.b, self.g, self.r)
            elif tipeMakeUp == 'pipi' :
                self.face.setPoint(my_points[2:3], my_points[14:15])
                # kiri 2, 5
                self.face.getPoints(2, 3, my_points)
                self.face.point[0][0] = self.face.hitung1
                self.face.image = self.face.createBoxLips(self.imageDetector.image, self.face.point, 2, masked=True, cropped=False, tipe=tipeMakeUp)
                self.face.masking(self.imageDetector.original_image, self.b, self.g, self.r)
                
                # kanan 12, 15
                self.face.getPoints(14, 15, my_points)
                self.face.point[0][0] = self.face.hitung2
                self.face.image = self.face.createBoxLips(self.imageDetector.image, self.face.point, 2, masked=True, cropped=False, tipe=tipeMakeUp)
                self.face.masking(self.face.color, self.b, self.g, self.r)
            elif tipeMakeUp == 'mata' :
                # kiri
                self.face.getPoints(36, 42, my_points)
                self.face.image = self.face.createBoxLips(self.imageDetector.image, self.face.point, 2, masked=True, cropped=False, tipe=tipeMakeUp)
                self.face.masking(self.imageDetector.original_image, self.b, self.g, self.r)
                
                # kanan
                self.face.getPoints(42, 47, my_points)
                self.face.image = self.face.createBoxLips(self.imageDetector.image, self.face.point, 2, masked=True, cropped=False, tipe=tipeMakeUp)
                self.face.masking(self.face.color, self.b, self.g, self.r)
            elif tipeMakeUp == 'alis' :
                # kiri
                self.face.getPoints(17, 22, my_points)
                self.face.image = self.face.createBoxLips(self.imageDetector.image, self.face.point, 2, masked=True, cropped=False, tipe=tipeMakeUp)
                self.face.masking(self.imageDetector.original_image, self.b, self.g, self.r)
                
                # kanan
                self.face.getPoints(22, 27, my_points)
                self.face.image = self.face.createBoxLips(self.imageDetector.image, self.face.point, 2, masked=True, cropped=False, tipe=tipeMakeUp)
                self.face.masking(self.face.color, self.b, self.g, self.r)
        # end image filter
    
        cv2.imwrite(self.imageDetector.link, self.face.color)
        