from django.conf import settings
from django.db import models
from routes.models import Route
from vehicles.models import Vehicle


class TripStatus(models.TextChoices):
    DRAFT = 'DRAFT', 'Brouillon'
    PUBLISHED = 'PUBLISHED', 'Publié'
    FULL = 'FULL', 'Complet'
    CANCELLED = 'CANCELLED', 'Annulé'
    COMPLETED = 'COMPLETED', 'Terminé'


class TripOffer(models.Model):
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trip_offers')
    route = models.ForeignKey(Route, on_delete=models.PROTECT, related_name='offers')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT, related_name='offers')
    date_depart = models.DateField()
    heure_depart = models.TimeField()
    places_totales = models.PositiveSmallIntegerField()
    places_disponibles = models.PositiveSmallIntegerField()
    prix_unitaire = models.PositiveIntegerField(help_text='Prix unitaire en FCFA')
    statut = models.CharField(max_length=20, choices=TripStatus.choices, default=TripStatus.DRAFT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Offre de trajet'
        verbose_name_plural = 'Offres de trajet'
        ordering = ['-date_depart', '-heure_depart']

    def __str__(self):
        # Représentation lisible d'une offre de trajet
        return f"{self.route} — {self.date_depart} {self.heure_depart} — {self.places_disponibles}/{self.places_totales}"

    def save(self, *args, **kwargs):
        # Règles métier appliquées côté serveur :
        # - Le prix unitaire est toujours récupéré depuis l'itinéraire (`Route`) pour éviter toute manipulation côté client.
        # - Au moment de la création, `places_disponibles` est initialisé à `places_totales` si non renseigné.
        if not self.prix_unitaire and self.route:
            self.prix_unitaire = self.route.prix
        if not self.places_disponibles:
            self.places_disponibles = self.places_totales
        super().save(*args, **kwargs)

    def is_full(self):
        """Retourne True si l'offre est complète (aucune place disponible)."""
        return self.places_disponibles <= 0
