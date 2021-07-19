from itertools import chain

from django.contrib import admin
from django import forms

from .models import Contrat, Event, Client
from user.models import User

admin.AdminSite.site_header = 'EPIC Event administration'
admin.AdminSite.site_title = 'EPIC Event'


class EventForm(forms.ModelForm):
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

        if isinstance(self.cleaned_data['support_contact'], User):
            if self.cleaned_data['event_status'] == 'Créé':
                self.instance.event_status = 'Affecté'
                self.instance.save()
                self._save_m2m()
        return self.instance


class ContratForm(forms.ModelForm):
    class Meta:
        model = Contrat
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
    form = EventForm
    readonly_fields = [
        'date_created', 'date_updated'
    ]
    fieldsets = [
        ('Suivi par', {'fields': ['contrat', 'support_contact', ]}),
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
        user = request.user.id
        # Si l'evenement est fini et que ce n'est pas l'equipe de Gestion qui consulte ==> Lecture Seule
        if not request.user.team == "Equipe de gestion" and obj.event_status == 'Terminé':
            return [f.name for f in self.model._meta.fields]
        # Ce n'est pas l'equipe de Gestion et que ce n'est pas la personne affecte ou le commercial ==> Lecture Seule
        elif not request.user.team == "Equipe de gestion" \
                and user != obj.support_contact_id and user != obj.contrat.sales_contact_id:
            return [f.name for f in self.model._meta.fields]

        return super(EventAdmin, self).get_readonly_fields(
            request, obj=obj
        )


class EventInline(admin.TabularInline):
    model = Event


class ContratAdmin(admin.ModelAdmin):
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
        if not request.user.is_superuser and obj.status is True:
            return [f.name for f in self.model._meta.fields]
        return super(ContratAdmin, self).get_readonly_fields(
            request, obj=obj
        )


class ClientAdmin(admin.ModelAdmin):
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


admin.site.register(Client, ClientAdmin)
admin.site.register(Contrat, ContratAdmin)
admin.site.register(Event, EventAdmin)
