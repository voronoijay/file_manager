from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage

class fileManager(models.Model):
    worksheet_name = models.CharField(max_length= 150, default = True)
    
    my_file = models.FileField(upload_to = 'sub_dir', default = True, storage=FileSystemStorage(location='/mnt/hdd2/jay_test'))
