import os
import uuid
from django.db import models

# Create your models here.
def user_directory_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('images/', filename)

class Images(models.Model):
    uid = models.CharField(max_length=50)
    tipeMakeUp = models.CharField(max_length=50, default='lips')
    colorR = models.IntegerField(default=255)
    colorG = models.IntegerField(default=0)
    colorB = models.IntegerField(default=0)
    images = models.ImageField(
        upload_to=user_directory_path
    )