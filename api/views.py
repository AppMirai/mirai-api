import os

from core.settings import MEDIA_ROOT
from rest_framework import generics
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView
from rest_framework.response import Response
from api.custom_renderers import JPEGRender
from api.proses import Proses
import api.newProses as newProses
from images.models import Images
from images.serializers import ImagesSerializer

# Create your views here.
class ImageAPIView(generics.RetrieveAPIView):
    renderer_classes = [JPEGRender]

    def get(self, request, *args, **kwargs):
        # tipeMakeUp = Images.objects.get(uid=kwargs['uid']).tipeMakeUp
        # warna = [Images.objects.get(uid=kwargs['uid']).colorR, Images.objects.get(uid=kwargs['uid']).colorG, Images.objects.get(uid=kwargs['uid']).colorB];
        # proses = Proses(warna, tipeMakeUp, request, *args, **kwargs)
        queryset = Images.objects.get(uid=kwargs['uid']).images

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
            tipeMakeUp = str(image_serializer.data.get('tipeMakeUp'))
            warna = [image_serializer.data.get('colorR'), image_serializer.data.get('colorG'),image_serializer.data.get('colorB')]
            query = image_serializer.data.get('images')
            proses = newProses.Proses(warna, tipeMakeUp, query)
            return Response(
                image_serializer.data
            )
        else:
            return Response(
                image_serializer.errors
            )

class DeleteImage(RetrieveDestroyAPIView):
    lookup_field = 'uid'
    serializer_class = ImagesSerializer
    def get_queryset(self):
        queryset = Images.objects.all()
        return queryset
    def delete(self, request, *args, **kwargs):
        link = str(MEDIA_ROOT) + '/' + str(Images.objects.get(uid=self.kwargs['uid']).images)
        os.remove(path=link)
        return self.destroy(request, *args, **kwargs)