from django.db import models
from usersApp.models import CustomUser 

class Card(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    word = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    meaning = models.TextField(default="Not specified")

    def __str__(self):
        return self.word








class Notification(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message