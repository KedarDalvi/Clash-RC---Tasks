from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    use_name = models.OneToOneField(User, on_delete = models.CASCADE, max_length = 50)
    ph_no = models.IntegerField(max_length = 10)

    def __str__(self):
        return self.f_name + ' ' + self.l_name




