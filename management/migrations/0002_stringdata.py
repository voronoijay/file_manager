# Generated by Django 3.2.4 on 2021-10-20 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StringData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('string_a', models.CharField(default=True, max_length=300)),
                ('string_b', models.CharField(default=True, max_length=300)),
                ('string_c', models.CharField(default=True, max_length=300)),
                ('string_d', models.CharField(default=True, max_length=300)),
                ('string_e', models.CharField(default=True, max_length=300)),
            ],
        ),
    ]
