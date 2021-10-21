from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

class FileManager(models.Model):
    worksheet_name = models.CharField(max_length= 150, default = True)
    
    my_file = models.FileField(upload_to = 'sub_dir', default = True, storage=FileSystemStorage(location='/mnt/hdd2/jay_test'))

class StringData(models.Model):
    string_a = models.CharField(max_length= 300, default = True)
    string_b = models.CharField(max_length= 300, default = True)
    string_c = models.CharField(max_length= 300, default = True)
    string_d = models.CharField(max_length= 300, default = True)
    string_e = models.CharField(max_length= 300, default = True)
    