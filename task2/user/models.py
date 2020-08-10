from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):

    f_name = models.CharField(max_length = 30, blank = True)
    l_name = models.CharField(max_length = 30, blank = True)
    email = models.CharField(max_length = 30, blank = True)
    ph_no = models.CharField(max_length = 10, blank = True)
    gender = models.CharField(max_length = 10, blank = True)

    def __str__(self):
        return self.f_name + " " + self.l_name

