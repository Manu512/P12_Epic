""" views.pu"""
import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .models import Contrat, Event, Client
from .permissions import VendorTeam, SupportTeam
from .serializers import ClientSerializer, EventSerializer, ContratSerializer

logger = logging.getLogger(__name__)


# Create your views here.
def log(content):
    """
    Function to log event
    :param content: Detail explaining why this entry
    """
    logger.error(content.values())


class ClientViewSet(viewsets.ModelViewSet):
    """
    API Client endpoint which displays a list of all clients.
    """
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated, VendorTeam]
    filterset_fields = ['last_name', 'email']

    def get_queryset(self):
        return Client.objects.all()

    def destroy(self, request, *args, **kwargs):
        content = {"detail": "Client can't be deleted with the api."}
        log(content)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ContratViewSet(viewsets.ModelViewSet):
    """
    API Contract endpoint which displays a list of all Contracts.
    """
    serializer_class = ContratSerializer
    permission_classes = [permissions.IsAuthenticated, VendorTeam]

    def get_queryset(self):
        queryset = Contrat.objects.all()
        client = self.request.query_params.get('client')
        if client is not None:
            queryset = queryset.filter(client__last_name__icontains=client)

        date = self.request.query_params.get('date')
        if date is not None:
            queryset = queryset.filter(client__contrat__date_created__day=date)

        amount = self.request.query_params.get('amount')
        if amount is not None:
            queryset = queryset.filter(client__contrat__amount=amount)

        return queryset

    def destroy(self, request, *args, **kwargs):
        content = {"detail": "Contrat can't be deleted with the api."}
        log(content)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class EventViewSet(viewsets.ModelViewSet):
    """
    API Event endpoint which displays a list of all Events.
    """
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated, SupportTeam]
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['event_date']

    def get_queryset(self):
        queryset = Event.objects.all()
        client = self.request.query_params.get('client')
        if client is not None:
            queryset = queryset.filter(client__last_name__icontains=client)

        email = self.request.query_params.get('email')
        if email is not None:
            queryset = queryset.filter(client__email__icontains=email)
        return queryset

    def destroy(self, request, *args, **kwargs):
        content = {"detail": "Event can't be deleted with the api."}
        log(content)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
