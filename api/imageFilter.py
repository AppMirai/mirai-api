import os

from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from api.custom_renderers import JPEGRender
from api.face import Face
from api.imageDetector import ImageDetector
# from api.imageDetector import ImageDetector
from core.settings import PROJECT_ROOT, MEDIA_ROOT

from images.models import Images
from images.serializers import ImagesSerializer

import cv2
import numpy as np
import dlib


class ImageFilter():
    def __init__(self, request, *args, **kwargs):
        self.queryset = Images.objects.get(uid=kwargs['uid']).images
        self.uid = str(Images.objects.get(uid=kwargs['uid']).uid)
        self.r = 255
        self.g = 0
        self.b = 0
        
        # image detector
        self.face_datasets = os.path.join(PROJECT_ROOT, 'shape_predictor_68_face_landmarks.dat')
        self.data_link = str(self.queryset)
        self.base_directory = str(MEDIA_ROOT)
        self.image_copy = self.base_directory + '/images/' + self.uid + 'cpy.jpg'
        self.link = self.base_directory + '/' + self.data_link
        
        if(os.path.exists(str(self.image_copy))):
            self.image = cv2.imread(self.image_copy)
        else:
            original_image = cv2.imread(self.link)
            cv2.imwrite(self.image_copy, original_image)
            self.image = cv2.imread(self.image_copy)

        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.face_datasets)
        self.original_image = self.image.copy()
        self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.faces = self.detector(self.gray_image)
        
    def faceFilter(self, p1, p2, my_points) :
        return Face(p1, p2, my_points)
    
    def imageDetector() :
        return ImageDetector
        