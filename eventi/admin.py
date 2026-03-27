from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utente, Location, Artista, Servizio, Evento, EventoArtista, EventoServizio, Ticket


@admin.register(Utente)
class UtenteAdmin(UserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_organizzatore']
    fieldsets = UserAdmin.fieldsets + (
        ('Profilo', {'fields': ('telefono', 'is_organizzatore')}),
    )


class EventoArtistaInline(admin.TabularInline):
    model = EventoArtista
    extra = 1


class EventoServizioInline(admin.TabularInline):
    model = EventoServizio
    extra = 1


@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ['titolo', 'organizzatore', 'location', 'data_inizio', 'stato']
    list_filter = ['stato', 'data_inizio']
    inlines = [EventoArtistaInline, EventoServizioInline]


admin.site.register(Location)
admin.site.register(Artista)
admin.site.register(Servizio)
admin.site.register(Ticket)