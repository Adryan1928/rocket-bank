from django.db import models
from users.models import Client

# Create your models here.
class Pix(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    key = models.CharField(max_length=255, unique=True)

class Favorite(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    pix = models.ManyToManyField(Pix, related_name='favorited_by')
