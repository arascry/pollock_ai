from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
from datetime import date
from django.contrib.auth.models import User
# Create your models here.
class Painting(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    urls = ArrayField(base_field=models.URLField())

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.id })

class Word(models.Model):
    word = models.CharField(max_length=100)
    seed = models.CharField(max_length=100)
    instruction = ArrayField(base_field=models.IntegerField())
    max_step = ArrayField(base_field=models.IntegerField())