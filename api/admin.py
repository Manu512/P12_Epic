from django.contrib import admin

from .models import Contrat, Event, Client


admin.AdminSite.site_header = 'EPIC Event administration'

class EventAdmin(admin.ModelAdmin):
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
    list_display = ['event_date', 'client', 'date_updated', 'event_status', ]
    list_filter = ('client', 'support_contact', 'event_status', 'event_date')
    search_fields = ('client', 'support_contact',)
    ordering = ('event_date',)
    # def get_readonly_fields(self, request, obj=None):
    #     if not request.user.team == "Equipe Gestion" and request.user.id == obj.support_contact_id:
    #         return [f.name for f in self.model._meta.fields]
    #     return super(EventAdmin, self).get_readonly_fields(
    #             request, obj=obj
    #     )

class EventInline(admin.TabularInline):
    model = Event

class ContratAdmin(admin.ModelAdmin):
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
    list_display = ['company_name', 'date_updated', 'prospect', ]
    list_filter = ('prospect', 'company_name', 'date_updated', 'date_created')
    search_fields = ('first_name', 'last_name', 'email',)
    ordering = ('date_created',)


admin.site.register(Client, ClientAdmin)
admin.site.register(Contrat, ContratAdmin)
admin.site.register(Event, EventAdmin)
