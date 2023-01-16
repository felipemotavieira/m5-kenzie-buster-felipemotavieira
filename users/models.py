from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    birthdate = models.DateField(null=True, blank=True)
    is_employee = models.BooleanField(default=False, null=True)
