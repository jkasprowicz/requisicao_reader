from django.db import models

# Create your models here.


class Exam(models.Model):
    name = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    paciente_nome = models.CharField(max_length=255)
    convenio = models.CharField(max_length=255)
    


    def __str__(self):
        return self.name