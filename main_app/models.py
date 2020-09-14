from django.db import models
from django.urls import reverse
from django.contrib.postgres.fields import ArrayField
# Create your models here.
class Painting(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    urls = models.ArrayField(base_field=models.URLField())
