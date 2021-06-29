""" views.pu"""
from rest_framework import viewsets, permissions, status
from .models import Contrat, Event, Client
from rest_framework.response import Response


# Create your views here.
class ContratViewSet(viewsets.ModelViewSet):
    pass

class ClientViewSet(viewsets.ModelViewSet):
    pass

class EventViewSet(viewsets.ModelViewSet):
    pass
