"""models.py"""

from phonenumber_field.modelfields import PhoneNumberField
from django.conf import settings
from django.db import models


class TimeStampModel(models.Model):
    """
    Définition d'un objet abstrait pour définir un héritage par la suite.
    Evite la répétition car le champ time_created est présent dans plusieurs modèle/classe.
    """
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Client(TimeStampModel):
    """
    Définition de l'objet Client
    """
    first_name = models.CharField('Prénom', max_length=25)
    last_name = models.CharField('Nom', max_length=25)
    email = models.EmailField()
    phone = PhoneNumberField()
    company_name = models.CharField('Compagnie', max_length=250)
    sales_contact = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='sales_by', on_delete=models.CASCADE)
    prospect = models.BooleanField(default=True)

    def __str__(self):
        return "{} {} from {} Phone : {}".format(self.last_name, self.first_name, self.company_name, self.phone)


class Contrat(TimeStampModel):
    """
    Définition de l'objet Contract
    """
    sales_contact = models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='sold_by', on_delete=models.CASCADE)
    client = models.ForeignKey(to='Client', on_delete=models.CASCADE)
    status = models.BooleanField()
    amount = models.FloatField()
    payement_due = models.DateTimeField()


class Event(TimeStampModel):
    """
    Définition de l'objet Event
    """
    client = models.ForeignKey(to='Client', on_delete=models.CASCADE)
    support_contact = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                        related_name='support_by')
    event_date = models.DateTimeField()

    class EventStatus(models.TextChoices):
        NEW = 'Nouveau'
        IN_PROGRESS = 'En Préparation'
        ENDED = 'Terminé'

    event_status = models.CharField(max_length=20 ,choices=EventStatus.choices, default=EventStatus.NEW)
    attendees = models.PositiveIntegerField()
    notes = models.TextField(max_length=2048, blank=True)

    class Meta:
        ordering = ['event_date']


    class Team(models.TextChoices):
        MANAGER = 'Equipe de gestion'
        VENDOR = 'Equipe commerciale'
        SUPPORT = 'Equipe support'

    team = models.CharField(max_length=20, choices=Team.choices, default=Team.MANAGER)