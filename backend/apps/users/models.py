from django.contrib.auth.models import AbstractUser
from django.db import models

# Custom User Model
class Teacher(AbstractUser):
    school_name = models.CharField(max_length=120, blank=True)
