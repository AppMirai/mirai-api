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
        data = queryset

        dat = os.path.join(PROJECT_ROOT, 'shape_predictor_68_face_landmarks.dat')
        dataLink = str(data)
        baseDir = str(MEDIA_ROOT)

        link = baseDir + '/' + dataLink

        img = cv2.imread(link)

        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(dat)


        r = 0
        g = 0
        b = 0

        def createBoxLips(img, points, scale=5, masked=False, cropped=True):
            if masked:
                mask = np.zeros_like(img)
                # block
                mask = cv2.fillPoly(mask, [points], (255, 255, 255))
                # line
                # mask = cv2.polylines(mask, [points], False, (255, 255, 255), thickness=10)
                # img = cv2.bitwise_and(img, mask)
                # cv2.imshow('Mask', img)

            if cropped:
                bbox = cv2.boundingRect(points)
                x, y, w, h = bbox
                imgCrop = img[y:y + h, x:x + w]
                imgCrop = cv2.resize(imgCrop, (0, 0), None, scale, scale)
                return imgCrop

            else:
                return mask

        # foto
        imgOriginal = img.copy()
        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector(imgGray)

        for face in faces:
            x1, y1 = face.left(), face.top()
            x2, y2 = face.right(), face.bottom()
            # tampilan bounding box
            # imgOriginal = cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            landmarks = predictor(imgGray, face)
            myPoints = []
            for n in range(68):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                myPoints.append([x, y])

            myPoints = np.array(myPoints)
            print(myPoints[48:61])
            imgLips = createBoxLips(img, myPoints[48:61], 2, masked=True, cropped=False)

            imgColorLips = np.zeros_like(imgLips)
            imgColorLips[:] = b, g, r
            imgColorLips = cv2.bitwise_and(imgLips, imgColorLips)
            imgColorLips = cv2.GaussianBlur(imgColorLips, (7, 7), 10)
            imgColorLips = cv2.addWeighted(imgOriginal, 1, imgColorLips, 0.4, 0)
            img = imgColorLips

        cv2.imwrite(link, imgColorLips)

        return Response(data, content_type='image/jpg')

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

