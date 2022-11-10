import os

from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from api.custom_renderers import JPEGRender
from core.settings import PROJECT_ROOT, MEDIA_ROOT

from images.models import Images
from images.serializers import ImagesSerializer

import cv2
import numpy as np
import dlib

# Create your views here.
class ImageAPIView(generics.RetrieveAPIView):
    renderer_classes = [JPEGRender]

    def get(self, request, *args, **kwargs):
        queryset = Images.objects.get(uid=self.kwargs['uid']).images
        uid = str(Images.objects.get(uid=self.kwargs['uid']).uid)
        #Start Bikin Class baru
        face_datasets = os.path.join(PROJECT_ROOT, 'shape_predictor_68_face_landmarks.dat')

        data_link = str(queryset)
        base_directory = str(MEDIA_ROOT)
        image_copy = base_directory + '/images/' + uid + 'cpy.jpg'
        link = base_directory + '/' + data_link

        if(os.path.exists(str(image_copy))):
            image = cv2.imread(image_copy)
        else:
            original_image = cv2.imread(link)
            cv2.imwrite(image_copy, original_image)
            image = cv2.imread(image_copy)

        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(face_datasets)

        print('------------------- DETECTOR')
        print(detector)
        print('--------------------')

        print('------------------ PREDITOR')
        print(predictor)
        print('--------------------')

        r = 255
        g = 0
        b = 0

        def createBoxLips(img, points, scale=5, masked=False, cropped=True):
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

        # foto
        original_image = image.copy()
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = detector(gray_image)
        print('--------------------- IMAGE')
        print(gray_image)
        print('----------------------')
        print('-------------------- FACES')
        print(faces)
        print('--------------------')

        for face in faces:
            x1, y1 = face.left(), face.top()
            x2, y2 = face.right(), face.bottom()
            landmarks = predictor(gray_image, face)
            my_points = []
            for n in range(68):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                my_points.append([x, y])

            my_points = np.array(my_points)
            image_lips = createBoxLips(image, my_points[48:61], 2, masked=True, cropped=False)

            image_color_lips = np.zeros_like(image_lips)
            image_color_lips[:] = b, g, r
            image_color_lips = cv2.bitwise_and(image_lips, image_color_lips)
            image_color_lips = cv2.GaussianBlur(image_color_lips, (7, 7), 10)
            image_color_lips = cv2.addWeighted(original_image, 1, image_color_lips, 0.4, 0)
            image = image_color_lips

        cv2.imwrite(link, image_color_lips)
        #end bikin class baru

        return Response(queryset, content_type='image/jpg')

class ImageUploadView(ListAPIView): 
    serializer_class = ImagesSerializer

    def get_queryset(self):
        queryset = Images.objects.all()
        return queryset

    def post(self, request, *args, **kwargs):
        image_serializer = ImagesSerializer(data=request.data)
        if image_serializer.is_valid():
            image_serializer.save()
            return Response(
                image_serializer.data
            )
        else:
            return Response(
                image_serializer.errors
            )

