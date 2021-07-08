""" views.pu"""
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .models import Contrat, Event, Client

from .serializers import ClientSerializer, EventSerializer, ContratSerializer
from .permissions import VendorTeam, SupportTeam


# Create your views here.
class ClientViewSet(viewsets.ModelViewSet):
    """
    API Client endpoint which displays a list of all clients.
    """
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated, VendorTeam, SupportTeam]

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ContratViewSet(viewsets.ModelViewSet):
    """
    API Contract endpoint which displays a list of all Contracts.
    """
    serializer_class = ContratSerializer
    permission_classes = [permissions.IsAuthenticated, VendorTeam, SupportTeam]

    def get_queryset(self):
        return Contrat.objects.all()

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class EventViewSet(viewsets.ModelViewSet):
    """
    API Event endpoint which displays a list of all Events.
    """
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated, VendorTeam, SupportTeam]

    def get_queryset(self):
        return Event.objects.all()

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_401_UNAUTHORIZED)