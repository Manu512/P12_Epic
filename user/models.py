from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Team(models.TextChoices):
        MANAGER = 'Equipe de gestion'
        VENDOR = 'Equipe commerciale'
        SUPPORT = 'Equipe support'

    team = models.CharField(max_length=20, choices=Team.choices, default=Team.MANAGER)

    class Meta:
        ordering = ['id']