from rest_framework import serializers
from .models import Utente, Location, Artista, Servizio, Evento, EventoArtista, EventoServizio, Ticket


class UtenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utente
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'telefono', 'is_organizzatore']
        read_only_fields = ['id']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class ArtistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artista
        fields = '__all__'


class ServizioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servizio
        fields = '__all__'


class EventoArtistaSerializer(serializers.ModelSerializer):
    artista = ArtistaSerializer(read_only=True)
    artista_id = serializers.PrimaryKeyRelatedField(
        queryset=Artista.objects.all(), source='artista', write_only=True
    )

    class Meta:
        model = EventoArtista
        fields = ['id', 'artista', 'artista_id', 'ruolo', 'cachet', 'orario_esibizione']


class EventoServizioSerializer(serializers.ModelSerializer):
    servizio = ServizioSerializer(read_only=True)
    servizio_id = serializers.PrimaryKeyRelatedField(
        queryset=Servizio.objects.all(), source='servizio', write_only=True
    )

    class Meta:
        model = EventoServizio
        fields = ['id', 'servizio', 'servizio_id', 'note', 'costo']


class EventoSerializer(serializers.ModelSerializer):
    organizzatore = UtenteSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    location_id = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all(), source='location', write_only=True
    )
    artisti = EventoArtistaSerializer(source='eventoartista_set', many=True, read_only=True)
    servizi = EventoServizioSerializer(source='eventoservizio_set', many=True, read_only=True)
    tickets_venduti = serializers.SerializerMethodField()

    class Meta:
        model = Evento
        fields = [
            'id', 'titolo', 'descrizione', 'data_inizio', 'data_fine',
            'stato', 'capienza_massima', 'organizzatore', 'location', 'location_id',
            'artisti', 'servizi', 'tickets_venduti', 'created_at'
        ]
        read_only_fields = ['organizzatore', 'created_at']

    def get_tickets_venduti(self, obj):
        return obj.tickets.filter(stato='acquistato').count()

    def create(self, validated_data):
        validated_data['organizzatore'] = self.context['request'].user
        return super().create(validated_data)


class TicketSerializer(serializers.ModelSerializer):
    evento = EventoSerializer(read_only=True)
    evento_id = serializers.PrimaryKeyRelatedField(
        queryset=Evento.objects.all(), source='evento', write_only=True
    )
    acquirente = UtenteSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'codice_univoco', 'tipo', 'prezzo', 'stato',
            'data_acquisto', 'evento', 'evento_id', 'acquirente'
        ]
        read_only_fields = ['codice_univoco', 'data_acquisto', 'acquirente', 'stato']

    def create(self, validated_data):
        validated_data['acquirente'] = self.context['request'].user
        return super().create(validated_data)