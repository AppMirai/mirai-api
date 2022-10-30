from distutils.log import warn
from rest_framework import generics
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from api.custom_renderers import JPEGRender
from api.proses import Proses
from images.models import Images
from images.serializers import ImagesSerializer

# Create your views here.
class ImageAPIView(generics.RetrieveAPIView):
    renderer_classes = [JPEGRender]

    def get(self, request, *args, **kwargs):
        tipeMakeUp = 'pipi'
        warna = [255, 0, 0];
        proses = Proses(warna, tipeMakeUp, request, *args, **kwargs)

        return Response(proses.imageDetector.queryset, content_type='image/jpg')


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

