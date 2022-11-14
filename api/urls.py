from django.urls import path
from .views import *

urlpatterns = [
    path('uid/<uid>', ImageAPIView.as_view()),
    path('add/', ImageUploadView.as_view()),
    path('delete/<uid>', DeleteImage.as_view())
]