# Generated by Django 4.2.13 on 2024-08-05 00:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ocr', '0003_textoextraido_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='image',
        ),
    ]
