import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class Utente(AbstractUser):
    telefono = models.CharField(max_length=20, blank=True)
    is_organizzatore = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"


class Location(models.Model):
    nome = models.CharField(max_length=200)
    indirizzo = models.CharField(max_length=300)
    citta = models.CharField(max_length=100)
    provincia = models.CharField(max_length=5)
    cap = models.CharField(max_length=5)
    capienza = models.PositiveIntegerField()
    accessibile = models.BooleanField(default=True)
    contatto = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.nome} – {self.citta}"

    class Meta:
        verbose_name_plural = "location"
        ordering = ['citta', 'nome']


class Artista(models.Model):
    nome_arte = models.CharField(max_length=200)
    nome_reale = models.CharField(max_length=200, blank=True)
    genere = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    contatto = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.nome_arte

    class Meta:
        ordering = ['nome_arte']


class Servizio(models.Model):
    TIPO_CHOICES = [
        ('navetta', 'Navetta'),
        ('audio', 'Audio/Tecnico'),
        ('catering', 'Catering'),
        ('sicurezza', 'Sicurezza'),
        ('fotografia', 'Fotografia/Video'),
        ('altro', 'Altro'),
    ]
    nome = models.CharField(max_length=200)
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, default='altro')
    descrizione = models.TextField(blank=True)
    fornitore = models.CharField(max_length=200, blank=True)
    contatto_fornitore = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"

    class Meta:
        ordering = ['tipo', 'nome']


class Evento(models.Model):
    STATO_CHOICES = [
        ('bozza', 'Bozza'),
        ('pubblicato', 'Pubblicato'),
        ('annullato', 'Annullato'),
        ('concluso', 'Concluso'),
    ]
    titolo = models.CharField(max_length=300)
    descrizione = models.TextField(blank=True)
    data_inizio = models.DateTimeField()
    data_fine = models.DateTimeField()
    stato = models.CharField(max_length=20, choices=STATO_CHOICES, default='bozza')
    capienza_massima = models.PositiveIntegerField()
    organizzatore = models.ForeignKey(
        'Utente', on_delete=models.CASCADE, related_name='eventi_organizzati'
    )
    location = models.ForeignKey(
        Location, on_delete=models.PROTECT, related_name='eventi'
    )
    artisti = models.ManyToManyField(
        Artista, through='EventoArtista', blank=True
    )
    servizi = models.ManyToManyField(
        Servizio, through='EventoServizio', blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titolo} – {self.data_inizio.date()}"

    class Meta:
        ordering = ['-data_inizio']


class EventoArtista(models.Model):
    RUOLO_CHOICES = [
        ('headliner', 'Headliner'),
        ('opening', 'Opening Act'),
        ('ospite', 'Ospite Speciale'),
        ('dj', 'DJ'),
        ('musicista', 'Musicista'),
        ('cantante', 'Cantante'),
        ('altro', 'Altro'),
    ]
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    artista = models.ForeignKey(Artista, on_delete=models.CASCADE)
    ruolo = models.CharField(max_length=50, choices=RUOLO_CHOICES, default='altro')
    cachet = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    orario_esibizione = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.artista} @ {self.evento} ({self.get_ruolo_display()})"

    class Meta:
        unique_together = ('evento', 'artista')


class EventoServizio(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    servizio = models.ForeignKey(Servizio, on_delete=models.CASCADE)
    note = models.TextField(blank=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.servizio} @ {self.evento}"

    class Meta:
        unique_together = ('evento', 'servizio')


class Ticket(models.Model):
    TIPO_CHOICES = [
        ('standard', 'Standard'),
        ('ridotto', 'Ridotto'),
        ('omaggio', 'Omaggio'),
        ('vip', 'VIP'),
        ('early_bird', 'Early Bird'),
    ]
    STATO_CHOICES = [
        ('acquistato', 'Acquistato'),
        ('annullato', 'Annullato'),
        ('usato', 'Usato'),
    ]
    codice_univoco = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='standard')
    prezzo = models.DecimalField(max_digits=8, decimal_places=2)
    stato = models.CharField(max_length=20, choices=STATO_CHOICES, default='acquistato')
    data_acquisto = models.DateTimeField(auto_now_add=True)
    evento = models.ForeignKey(Evento, on_delete=models.PROTECT, related_name='tickets')
    acquirente = models.ForeignKey(
        'Utente', on_delete=models.PROTECT, related_name='tickets_acquistati'
    )

    def __str__(self):
        return f"[{self.get_tipo_display()}] {self.evento} – {self.acquirente}"

    class Meta:
        ordering = ['-data_acquisto']