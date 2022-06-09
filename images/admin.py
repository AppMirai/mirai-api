from django.contrib import admin
from . import models

# Register your models here.

@admin.register(models.Images)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('uid', 'id')

