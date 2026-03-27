from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Utente, Location, Artista, Servizio, Evento, Ticket
from .serializers import (
    UtenteSerializer, LocationSerializer, ArtistaSerializer,
    ServizioSerializer, EventoSerializer, TicketSerializer
)


class IsOrganizzatoreOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_organizzatore


class UtenteViewSet(viewsets.ModelViewSet):
    queryset = Utente.objects.all()
    serializer_class = UtenteSerializer
    permission_classes = [permissions.IsAdminUser]

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        return Response(UtenteSerializer(request.user).data)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsOrganizzatoreOrReadOnly]


class ArtistaViewSet(viewsets.ModelViewSet):
    queryset = Artista.objects.all()
    serializer_class = ArtistaSerializer
    permission_classes = [IsOrganizzatoreOrReadOnly]


class ServizioViewSet(viewsets.ModelViewSet):
    queryset = Servizio.objects.all()
    serializer_class = ServizioSerializer
    permission_classes = [IsOrganizzatoreOrReadOnly]


class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.select_related('organizzatore', 'location').prefetch_related(
        'artisti', 'servizi', 'tickets'
    )
    serializer_class = EventoSerializer
    permission_classes = [IsOrganizzatoreOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        stato = self.request.query_params.get('stato')
        citta = self.request.query_params.get('citta')
        if stato:
            qs = qs.filter(stato=stato)
        if citta:
            qs = qs.filter(location__citta__icontains=citta)
        return qs


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Ticket.objects.all()
        return Ticket.objects.filter(acquirente=user)