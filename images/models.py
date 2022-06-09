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
    images = models.ImageField(
        upload_to=user_directory_path
    )