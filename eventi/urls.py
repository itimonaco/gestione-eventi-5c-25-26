from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('utenti', views.UtenteViewSet)
router.register('location', views.LocationViewSet)
router.register('artisti', views.ArtistaViewSet)
router.register('servizi', views.ServizioViewSet)
router.register('eventi', views.EventoViewSet)
router.register('tickets', views.TicketViewSet, basename='ticket')

urlpatterns = [
    path('', include(router.urls)),
]