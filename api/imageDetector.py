from asyncio.windows_events import NULL
import os

from core.settings import PROJECT_ROOT, MEDIA_ROOT

from images.models import Images

import cv2
import dlib


class ImageDetector():
    def __init__(self, request, *args, **kwargs) :
        self.inisialisasiVar()
        self.getImage(request, *args, **kwargs)
        self.getDetector()
        self.detectioning()
        
        
    def inisialisasiVar(self) :
        self.queryset = 0
        self.uid = 0
        self.data_link = 0
        self.base_directory = 0
        self.image_copy = 0
        self.link = 0
        self.face_datasets = 0
        self.detector = 0
        self.predictor = 0
    
    
    def getImage(self, request, *args, **kwargs) :
        self.queryset = Images.objects.get(uid=kwargs['uid']).images
        self.uid = str(Images.objects.get(uid=kwargs['uid']).uid)
        self.data_link = str(self.queryset)
        self.base_directory = str(MEDIA_ROOT)
        self.image_copy = self.base_directory + '/images/' + self.uid + 'cpy.jpg'
        self.link = self.base_directory + '/' + self.data_link
    
        
    def getDetector(self) :
        self.face_datasets = os.path.join(PROJECT_ROOT, 'shape_predictor_68_face_landmarks.dat')
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(self.face_datasets)
    
    
    def detectioning(self) :
        if(os.path.exists(str(self.image_copy))):
            self.image = cv2.imread(self.image_copy)
        else:
            original_image = cv2.imread(self.link)
            cv2.imwrite(self.image_copy, original_image)
            self.image = cv2.imread(self.image_copy)

        self.original_image = self.image.copy()
        self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.faces = self.detector(self.gray_image)