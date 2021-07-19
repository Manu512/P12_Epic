from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.shortcuts import get_object_or_404

from .models import User

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)

        if commit:
            user.save()
        return get_object_or_404(User, pk=user.pk)

    class Meta:
        model = User
        fields = 'username', 'password'


class CustomUserAdmin(UserAdmin):
    model = User

    readonly_fields = [
        'last_login', 'date_joined'
    ]

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Info Personnel', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('team', 'is_active',  'is_staff', 'groups'),
        }),
        ('Historique', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'last_name',  'first_name', 'is_staff', 'team', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'first_name', 'last_name', 'team')
    list_filter = ('is_staff', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('date_joined',)
    filter_horizontal = ('groups', 'user_permissions',)



admin.site.register(User, CustomUserAdmin)


