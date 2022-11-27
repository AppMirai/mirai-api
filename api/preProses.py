import os

import numpy as np

from api.face import Face
from core.settings import PROJECT_ROOT, MEDIA_ROOT, BASE_DIR
import cv2
import dlib

class preProses():
    def __init__(self, query):
        self.inisialisasiVar()
        self.getImage(query)
        self.getDetector()
        self.detectioning()

    def inisialisasiVar(self):
        self.queryset = 0
        self.uid = 0
        self.data_link = 0
        self.base_directory = 0
        self.link = 0
        self.face_datasets = 0
        self.detector = 0
        self.predictor = 0

    def getImage(self, query):
        self.queryset = query
        print('=======================')
        print(self.queryset)
        print('=======================')
        self.data_link = str(self.queryset)
        self.base_directory = str(BASE_DIR)
        self.link = self.base_directory + self.data_link
        print('=======================')
        print(self.link)
        print('=======================')

    def getDetector(self) :
        self.face_datasets = os.path.join(PROJECT_ROOT, 'shape_predictor_68_face_landmarks.dat')
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.face_datasets)

    def detectioning(self) :
        self.image = cv2.imread(self.link)
        self.original_image = self.image.copy()
        self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.faces = self.detector(self.gray_image)
        print('=================== test')
        print(len(self.faces))
        print('===================')