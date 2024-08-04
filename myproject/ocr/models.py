from django.db import models


class UserProfile(models.Model):
    name = models.CharField(max_length=255)
    birth_date = models.DateField()
    cpf = models.CharField(max_length=11, unique=True)
    image = models.ImageField(upload_to='user_documents/')

    def __str__(self):
        return self.name

class Exam(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='exams')
    exames = models.CharField(max_length=255)
    image = models.ImageField(upload_to='exam_images/', null=True, blank=True) 

    def __str__(self):
        return self.exames
    
class TextoExtraido(models.Model):
    texto = models.CharField(max_length=300)
    