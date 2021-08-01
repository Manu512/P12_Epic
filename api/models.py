"""models.py"""

from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


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
    phone = PhoneNumberField(verbose_name='Téléphone')
    company_name = models.CharField('Compagnie', max_length=250)
    sales_contact = models.ForeignKey(verbose_name='Commercial', to=settings.AUTH_USER_MODEL,
                                      related_name='sales_by', on_delete=models.CASCADE,
                                      limit_choices_to={'groups__name': "Equipe commercial"}, )
    prospect = models.BooleanField(default=True)

    def __str__(self):
        return "{} - {} {} - {}".format(self.company_name, self.last_name, self.first_name, self.email)

    class Meta:
        ordering = ['company_name']
        verbose_name = "Client"
        verbose_name_plural = "Clients"


class Contrat(TimeStampModel):
    """
    Définition de l'objet Contract
    """
    sales_contact = models.ForeignKey(verbose_name='Commercial', to=settings.AUTH_USER_MODEL, related_name='sold_by',
                                      limit_choices_to={'groups__name': "Equipe commercial"}, on_delete=models.CASCADE)
    client = models.ForeignKey(to='Client', on_delete=models.CASCADE)
    status = models.BooleanField(verbose_name='Contrat signé')
    amount = models.FloatField(verbose_name='Montant')
    payement_due = models.DateField(verbose_name='Payement au')

    def __str__(self):
        if self.status:
            state = "Signé"
        else:
            state = "Négociation en cours"
        return "{} - {} - {}".format(self.client, self.sales_contact, state)

    class Meta:
        ordering = ['payement_due']
        verbose_name = "Contrat"
        verbose_name_plural = "Contrats"


class Event(TimeStampModel):
    """
    Définition de l'objet Event
    """
    contrat = models.OneToOneField(verbose_name='Contrat', to='Contrat', on_delete=models.CASCADE, primary_key=True,
                                   unique=True)
    client = models.ForeignKey(to='Client', on_delete=models.CASCADE)
    support_contact = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                        limit_choices_to={'groups__name': "Equipe support"},
                                        related_name='support_by', verbose_name='Assigné à', blank=True, null=True)
    event_date = models.DateTimeField(verbose_name="Date de l'événement", null=True, blank=True)

    class EventStatus(models.TextChoices):
        CREATE = 'Créé'
        AFFECTED = 'Affecté'
        ENDED = 'Terminé'

    event_status = models.CharField(max_length=20, choices=EventStatus.choices,
                                    default=EventStatus.CREATE, blank=False, null=False,
                                    verbose_name="Status de l'évenement")
    attendees = models.PositiveIntegerField(verbose_name='Personnes attendues', default=1)
    notes = models.TextField(max_length=2048, blank=True)

    def __str__(self):
        return "Date : {} Status : {} - Personnes : {} - Suivi par {}".format(self.event_date, self.event_status,
                                                                              self.attendees, self.support_contact)

    class Meta:
        ordering = ['event_date']
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
