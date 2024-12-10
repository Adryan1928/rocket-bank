from django.db import models

from users.models import Client

# Create your models here.
class Pix(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    key = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.type} - {self.key}"

class Payment(models.Model):
    sender = models.ForeignKey(Client, related_name='payments_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Client, related_name='payments_received', on_delete=models.CASCADE)
    value = models.FloatField()
    date = models.DateField(auto_now_add=True)
    pix = models.ForeignKey(Pix, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Payment from {self.sender} to {self.receiver} of {self.value} on {self.date}"

class Favorite(models.Model):
    user = models.ForeignKey(Client, on_delete=models.CASCADE)

    pix = models.ForeignKey(Pix, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"Favorite Pix {self.pix} for user {self.user}"
