from django.urls import path, include
from .views import *
from rest_framework import routers

urlpatterns = [
    path('uid/<uid>', ImageAPIView.as_view()),
    path('add/', ImageUploadView.as_view()),
    path('delete/<uid>', DeleteImage.as_view())
]