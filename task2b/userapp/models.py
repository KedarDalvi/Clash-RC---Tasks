from django.db import models
from django.contrib.auth.models import User, auth

class UserProfile(models.Model):
    username = models.OneToOneField(User, on_delete = models.CASCADE, max_length = 50)
    ph_no = models.IntegerField()

    def __str__(self):
        return self.username




