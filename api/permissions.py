""" Gestion des Permissions """
from rest_framework import permissions
from api.models import Contrat,Client,Event

def is_vendor(user):
    return user.groups.filter(name='Equipe commercial').exists()

def is_support(user):
    return user.groups.filter(name='Equipe support').exists()

def is_affected(user, obj):
    r = False
    if isinstance(obj, Client) or isinstance(obj, Contrat):
        if obj.sales_contact_id == user.id:
            r = True
    elif isinstance(obj, Event):
        if obj.support_contact_id == user.id:
            r = True
    return r



class VendorTeam(permissions.BasePermission):
    """
    Custom permission to only allow vendors of an object to view it.
    """
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        access = False
        if request.method in permissions.SAFE_METHODS:
            access = True
        elif is_affected(request.user, obj):
            access = True
        return access


class SupportTeam(permissions.BasePermission):
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        access = False
        if request.method in permissions.SAFE_METHODS:
            access = True
        elif is_affected(request.user, obj):
            access = True
        return access
