from django.contrib.auth import password_validation
from django.db import models
from django.contrib.auth.models import Group
from django.contrib import admin
# Create your models here.
from django.contrib.auth.models import AbstractUser, Group

vendor_group, created = Group.objects.get_or_create(name='Equipe commerciale')
support_group, created = Group.objects.get_or_create(name='Equipe support')
manager_group, created = Group.objects.get_or_create(name='Equipe de gestion')

class User(AbstractUser):

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None
        group = Group.objects.get(name=self.team)
        self.groups.add(group)

    class Team(models.TextChoices):
        MANAGER = 'Equipe de gestion'
        VENDOR = 'Equipe commerciale'
        SUPPORT = 'Equipe support'


    team = models.CharField(max_length=20, choices=Team.choices,
                            default=Team.MANAGER, verbose_name='Equipe',
                            null=False, blank=False)
    class Meta:
        ordering = ['id']
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
