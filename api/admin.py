"""api admin.py"""
from django import forms
from django.contrib import admin

from user.models import User
from .models import Contrat, Event, Client

admin.AdminSite.site_header = 'EPIC Event administration'
admin.AdminSite.site_title = 'EPIC Event'


class EventForm(forms.ModelForm):
    """
    Event Form object in the administration interface.
    Formulaire d'evenement dans l'interface d'administration.
    """

    class Meta:
        model = Event
        fields = '__all__'

    def save(self, commit=True):

        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate." % (
                    self.instance._meta.object_name,
                    'created' if self.instance._state.adding else 'changed',
                )
            )
        if commit:
            # If committing, save the instance and the m2m data immediately.
            self.instance.save()
            self._save_m2m()
        else:
            # If not committing, add a method to the form to allow deferred
            # saving of m2m data.
            self.save_m2m = self._save_m2m

        # Si le contrat est signé, on crée un evenement si celui ci n'existe pas encore.
        # De plus le client change de status, ce n'est plus un prospect

        if isinstance(self.instance.support_contact, User):
            if self.instance.event_status == 'Créé':
                self.instance.event_status = 'Affecté'
                self.instance.save()
                self._save_m2m()
        return self.instance


class ContratForm(forms.ModelForm):
    """
    Contract Form object in the administration interface.
    Formulaire des contrats dans l'interface d'administration.
    """

    class Meta:
        model = Contrat
        fields = '__all__'

    def save(self, commit=True):
        """
        Function to save a contract object and validate certain fields.
        For example if the contract is signed (status is true), the prospect is no longer a prospect but a customer.
        Similarly for the contract, if it is signed, an event must be attached to it.

        Fonction de sauvegarde d'un objet contrat et qui va valider certain champs.
        Par exemple si le contrat est signé (status is true), le prospect n'est plus un prospect mais un client.
        De meme pour le contrat, si il est signé, un event doit y etre rattaché.
        :param kwargs:
        :return:
        """
        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate." % (
                    self.instance._meta.object_name,
                    'created' if self.instance._state.adding else 'changed',
                )
            )
        if commit:
            # If committing, save the instance and the m2m data immediately.
            self.instance.save()
            self._save_m2m()
        else:
            # If not committing, add a method to the form to allow deferred
            # saving of m2m data.
            self.instance.sales_contact = self.instance.client.sales_contact
            self.instance.save()
            self.save_m2m = self._save_m2m

        # Si le contrat est signé, on crée un évènement si celui-ci n'existe pas encore.
        # De plus le client change de status, ce n'est plus un prospect

        if len(self.cleaned_data):
            if self.cleaned_data['status']:
                evt = Event.objects.filter(contrat_id=self.instance.pk).exists()
                if not evt:
                    Event.objects.create(contrat_id=self.instance.pk, client_id=self.instance.client.id)
                clt = Client.objects.get(id=self.instance.client.id)
                if clt.prospect:
                    clt.prospect = False
                    clt.save()
        return self.instance


class EventAdmin(admin.ModelAdmin):
    """
    Event object in the administration interface.
    Objet Evenement dans l'interface d'administration.
    """
    form = EventForm
    readonly_fields = [
        'date_created', 'date_updated'
    ]
    fieldsets = [
        ('Suivi par', {'fields': ['support_contact', ]}),
        ("Informations concernant l'événément", {'fields': [
            'client',
            'event_date',
            'event_status',
            'attendees',
            'notes',
        ]}),
    ]
    list_display = ['support_contact', 'event_date', 'client', 'event_status', 'date_updated']
    list_filter = ('client', 'support_contact', 'event_status', 'event_date')
    search_fields = ('client', 'support_contact',)
    ordering = ('event_date',)

    def get_readonly_fields(self, request, obj=None):
        """
        Function allowing to pass some attribute in read only according to the conditions defined below.
        Fonction permettant de passer certain attribut en lecture seule selon les conditions défini ci-dessous.
        :param request:
        :param obj:
        :return:
        """
        user = request.user.id
        # Si l'evenement est fini et que ce n'est pas l'equipe de Gestion qui consulte ==> Lecture Seule
        if not request.user.team == "Equipe de gestion" and obj.event_status == 'Terminé':
            return [f.name for f in self.model._meta.fields]
        # C'est le commercial affecté
        elif user == obj.contrat.sales_contact_id or user == obj.support_contact_id:

            return ['support_contact', 'client', 'contrat', 'support_contact']

        # Ce n'est pas l'equipe de Gestion et que ce n'est pas la personne affecte  ==> Lecture Seule
        elif not request.user.team == "Equipe de gestion" \
                and user != obj.support_contact_id and user != obj.contrat.sales_contact_id:

            read_only = [f.name for f in self.model._meta.fields]

            return read_only

        return super(EventAdmin, self).get_readonly_fields(
            request, obj=obj
        )


class EventInline(admin.TabularInline):
    model = Event


class ContratAdmin(admin.ModelAdmin):
    """
    Contract object in the administration interface.
    Objet Contrat dans l'interface d'administration.
    """
    form = ContratForm
    inlines = [
        EventInline,
    ]
    readonly_fields = [
        'sales_contact', 'date_created', 'date_updated'
    ]
    fieldsets = [
        ('Suivi par', {'fields': ['sales_contact', 'status', ]}),
        ('Informations', {'fields': ['client',
                                     'amount',
                                     'payement_due',
                                     ]}),
    ]
    list_display = ['client', 'date_updated', 'status', ]
    list_filter = ('client', 'status', 'date_updated', 'date_created')
    search_fields = ('client', 'sales_contact',)
    ordering = ('date_created',)

    def get_readonly_fields(self, request, obj=None):
        """
        Function allowing to pass some attribute in read only according to the conditions defined below.
        Fonction permettant de passer certain attribut en lecture seule selon les conditions défini ci-dessous.
        :param request:
        :param obj:
        :return:
        """
        if obj is not None:
            if not request.user.is_superuser and obj.status is True:
                return [f.name for f in self.model._meta.fields]
            return super(ContratAdmin, self).get_readonly_fields(
                request, obj=obj)
        else:
            return super(ContratAdmin, self).get_readonly_fields(
                request, obj=obj)


class ClientForm(forms.ModelForm):
    """
    Client Form object in the administration interface.
    Formulaire des clients dans l'interface d'administration.
    """

    class Meta:
        model = Client
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        # accéder de l'objet request n'importe où en utilisant self.request
        # access request anywhere in your form methods by using self.request
        super(ClientForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        """
        Function to save a Client object and add certain fields.

        Fonction de sauvegarde d'un objet client et qui va ajouter certains champs.
        Ajout dans le champ commercial l'objet User de la personne logué.
        """
        if self.errors:
            raise ValueError(
                "The %s could not be %s because the data didn't validate." % (
                    self.instance._meta.object_name,
                    'created' if self.instance._state.adding else 'changed',
                )
            )
        if commit:
            # If committing, save the instance and the m2m data immediately.
            self.instance.save()
            self._save_m2m()
        else:
            # If not committing, add a method to the form to allow deferred
            # saving of m2m data.
            self.instance.sales_contact = self.request.user
            self.instance.save()
            self.save_m2m = self._save_m2m
        return self.instance


class ClientAdmin(admin.ModelAdmin):
    """
    Client object in the administration interface.
    Objet Client dans l'interface d'administration.
    """
    form = ClientForm

    readonly_fields = [
        'date_created', 'date_updated', 'sales_contact'
    ]
    fieldsets = [
        ('Type de client', {'fields': ['prospect']}),
        ('Informations', {'fields': ['company_name',
                                     'last_name',
                                     'first_name',
                                     'email',
                                     'phone',
                                     'sales_contact',
                                     ]}),
    ]
    list_display = ['company_name', 'last_name', 'first_name', 'email', 'date_updated', 'prospect', ]
    list_filter = ('prospect', 'company_name', 'date_updated', 'date_created')
    search_fields = ('first_name', 'last_name', 'email',)
    ordering = ('date_created',)

    def get_form(self, request, obj=None, **kwargs):

        AdminForm = super(ClientAdmin, self).get_form(request, obj, **kwargs)

        class AdminFormWithRequest(AdminForm):
            def __new__(cls, *args, **kwargs):
                kwargs['request'] = request
                return AdminForm(*args, **kwargs)

        return AdminFormWithRequest


admin.site.register(Client, ClientAdmin)
admin.site.register(Contrat, ContratAdmin)
admin.site.register(Event, EventAdmin)
