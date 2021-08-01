from django.contrib.auth import password_validation
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from api.models import Client, Contrat, Event


# vendor_group, created = Group.objects.get_or_create(name='Equipe commerciale')
# support_group, created = Group.objects.get_or_create(name='Equipe support')
# manager_group, created = Group.objects.get_or_create(name='Equipe de gestion')


class User(AbstractUser):
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None
        self.groups.clear()
        Group.objects.get(name=self.team).user_set.add(self)

    def is_vendor(self):
        return self.groups.filter(name='Equipe commerciale').exists()

    def is_support(self):
        return self.groups.filter(name='Equipe support').exists()

    def is_management(self):
        return self.groups.filter(name='Equipe de gestion').exists()

    def is_affected(self, obj):
        r = False
        if isinstance(obj, Client):  # Object Client
            if obj.sales_contact_id == self.id:
                r = True
        elif isinstance(obj, Contrat) and obj.status is False:  # Object Contrat et Non Signé
            r = True
        elif isinstance(obj, Event) and not obj.event_status == 'Ended':  # Object Event
            if obj.support_contact_id == self.id:
                r = True
            elif Contrat.objects.get(pk=obj.pk).sales_contact_id == self.id:
                r = True
        return r

    class Team(models.TextChoices):
        MANAGER = 'Equipe de gestion'
        VENDOR = 'Equipe commerciale'
        SUPPORT = 'Equipe support'

    is_staff = models.BooleanField(
        _('staff status'),
        default=True,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    team = models.CharField(max_length=20, choices=Team.choices,
                            default=Team.MANAGER, verbose_name='Equipe',
                            null=False, blank=False)

    class Meta:
        ordering = ['id']
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
