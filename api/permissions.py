""" Gestion des Permissions """
from rest_framework import permissions
from api.models import Contrat,Client,Event



class VendorTeam(permissions.BasePermission):
    """
    Custom permission to only allow vendors of an object to view it.
    """

    def has_permission(self, request, view):
        access = False
        if request.method in permissions.SAFE_METHODS:
            access = True
        elif request.method == 'DELETE':
            access = False
        elif request.user.is_vendor() or request.user.is_management():
            access = True

        return access

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        access = False
        if request.method in permissions.SAFE_METHODS:
            access = True
        elif request.method == 'DELETE':
            access = False
        elif request.user.is_affected(obj) or request.user.is_management():
            access = True
        return access


class SupportTeam(permissions.BasePermission):
    def has_permission(self, request, view):
        access = False

        if request.method in permissions.SAFE_METHODS:
            access = True
        elif request.method == 'DELETE':
            access = False
        elif request.user.is_vendor() or request.user.is_management():
            access = True

        return access

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        access = False
        if request.method in permissions.SAFE_METHODS:
            access = True
        elif request.method == 'DELETE':
            access = False
        elif request.user.is_affected(obj) or request.user.is_management():
            access = True
        return access
