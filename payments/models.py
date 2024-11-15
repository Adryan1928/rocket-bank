from django.db import models
from users.models import Client

# Create your models here.
class Payment(models.Model):
    sender = models.ForeignKey(Client, related_name='payments_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Client, related_name='payments_received', on_delete=models.CASCADE)
    value = models.FloatField()
    date = models.DateField(auto_now_add=True)

class Pix(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    key = models.CharField(max_length=255, unique=True)

class Favorite(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    pix = models.ForeignKey(Pix, on_delete=models.CASCADE, null=True, blank=True)
