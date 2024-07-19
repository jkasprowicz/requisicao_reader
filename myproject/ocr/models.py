from django.db import models

# Create your models here.


class Exam(models.Model):
    exames = models.CharField(max_length=255)
    image = models.ImageField(upload_to='exam_images/', null=True)

    def __str__(self):
        return self.exames