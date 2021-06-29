""" urls.py """
from rest_framework_nested import routers
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from . import views

route = routers.SimpleRouter()
route.register(r'client', views.ClientViewSet, basename='client')

contrat_route = routers.NestedSimpleRouter(route, r'client', lookup='client')
contrat_route.register(r'contrat', views.ContratViewSet, basename='contrat')
event_route = routers.NestedSimpleRouter(contrat_route, r'contrat', lookup='contrat')
event_route.register(r'event', views.EventViewSet, basename='event')


urlpatterns = [
    path('', include(route.urls), name="client"),
    path('', include(contrat_route.urls), name="contrat"),
    path('', include(event_route.urls), name="event"),
    path('admin/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
