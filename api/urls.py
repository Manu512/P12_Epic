""" urls.py """
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)

from . import views

route = routers.DefaultRouter()

route.get_api_root_view().cls.__name__ = "Epic_Event"
route.get_api_root_view().cls.__doc__ = "Racine de l'API EPIC Event"

route.register(r'client', views.ClientViewSet, basename='client')
route.register(r'contrat', views.ContratViewSet, basename='contrat')
route.register(r'event', views.EventViewSet, basename='event')

urlpatterns = [
    path('', include(route.urls), name="client"),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
