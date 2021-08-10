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
        """
        Function to save a user and validate certain fields.
        Depending on the user's team, the user will be assigned to a group giving him
        particular authorizations

        Fonction de sauvegarde d'un utilisateur et qui va valider certain champs.
        Selon l'équipe de l'utilisateur, celui ci se vera attribuer dans un groupe lui donnant
        des autorisations particulieres
        :param kwargs:
        :return:
        """
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None
        self.groups.clear()
        Group.objects.get(name=self.team).user_set.add(self)

    def is_vendor(self):
        """
        Function that returns True if the user is in the "Equipe commerciale" group
        Fonction qui renvoie True si l'utilisateur est dans le groupe Equipe commerciale
        """
        return self.groups.filter(name='Equipe commerciale').exists()

    def is_support(self):
        """
        Function that returns True if the user is in the "Equipe support" group
        Fonction qui renvoie True si l'utilisateur est dans le groupe Equipe support
        """
        return self.groups.filter(name='Equipe support').exists()

    def is_management(self):
        """
        Function that returns True if the user is in the "Equipe de gestion" group
        Fonction qui renvoie True si l'utilisateur est dans le groupe Equipe de gestion
        """
        return self.groups.filter(name='Equipe de gestion').exists()

    def is_affected(self, obj):
        """
        Function that returns True if the user is assigned to the object (this can be a contract or an event)
        Fonction qui renvoie True si l'utilisateur est affecté à l'objet (cela peut etre un contrat ou un evenement)
        """
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
