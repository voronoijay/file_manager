# Generated by Django 3.2.4 on 2021-10-12 05:23

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('worksheet_name', models.CharField(default=True, max_length=150)),
                ('my_file', models.FileField(default=True, storage=django.core.files.storage.FileSystemStorage(location='/mnt/hdd2/jay_test'), upload_to='sub_dir')),
            ],
        ),
    ]
