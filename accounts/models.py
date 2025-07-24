from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    RECEPTIONIST = 'receptionist'
    MAINTAINER = 'maintainer'
    SUPERADMIN = 'superadmin'
    ROLE_CHOICES = [
        (RECEPTIONIST, 'Receptionist'),
        (MAINTAINER, 'Manutentore'),
        (SUPERADMIN, 'Super Admin'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    resort = models.ForeignKey('resort.Resort', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
from django.db import models

# Create your models here.
