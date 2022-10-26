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

from .face import *
from .image import *

# Create your views here.
#Comment 2

#LSP Overload function get
#OCP Kalau mau nambahin fitur edit mulut harus ngedit kode dibawah
class ImageAPIView(generics.RetrieveAPIView):
    renderer_classes = [JPEGRender]

    def get(self, request, *args, **kwargs):
        r = 255
        g = 0
        b = 0
        
        queryset = Images.objects.get(uid=self.kwargs['uid']).images
        uid = str(Images.objects.get(uid=self.kwargs['uid']).uid)
        
        # start refactor

        # start image process
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
        original_image = image.copy()
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = detector(gray_image)
        # end image process

        # image filter
        for face in faces:
            landmarks = predictor(gray_image, face)
            my_points = []
            for n in range(68):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                my_points.append([x, y])

            my_points = np.array(my_points)
            lips = Face(48, 61, my_points)
            lips.image = lips.createBoxLips(image, lips.point, 2, masked=True, cropped=False)
            lips.masking(original_image, b, g, r)

            leftEyeBrow = Face(17, 22, my_points)
            leftEyeBrow.image = lips.createBoxLips(image, leftEyeBrow.point, 2, masked=True, cropped=False)
            leftEyeBrow.masking(original_image, b, g, r)

            rightEyeBrow = Face(22, 27, my_points)
            rightEyeBrow.image = lips.createBoxLips(image, rightEyeBrow.point, 2, masked=True, cropped=False)
            rightEyeBrow.masking(leftEyeBrow.color, b, g, r)

            leftEye = Face(36, 42, my_points)
            leftEye.image = lips.createBoxLips(image, leftEye.point, 2, masked=True, cropped=False)
            leftEye.masking(original_image, b, g, r)

            rightEye = Face(42, 47, my_points)
            rightEye.image = lips.createBoxLips(image, rightEye.point, 2, masked=True, cropped=False)
            rightEye.masking(leftEye.color, b, g, r)

            leftCheek = Face(2, 5, my_points)
            leftCheek.image = lips.createBoxLips(image, leftCheek.point, 2, masked=True, cropped=False)
            leftCheek.masking(original_image, b, g, r)

            rightCheek = Face(12, 15, my_points)
            rightCheek.image = lips.createBoxLips(image, rightCheek.point, 2, masked=True, cropped=False)
            rightCheek.masking(leftCheek.color, b, g, r)
        # end image filter

        cv2.imwrite(link, lips.color)
        # end refactor

        return Response(queryset, content_type='image/jpg')

#LSP soalnya ListAPIView punya function 'get' yang gk di pake
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

