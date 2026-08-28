from django.conf import settings
from django.db import models


class BookingStatus(models.TextChoices):
    """Statuts possibles d'une réservation."""
    PENDING = 'PENDING', 'En attente'
    CONFIRMED = 'CONFIRMED', 'Confirmée'
    CANCELLED = 'CANCELLED', 'Annulée'
    REJECTED = 'REJECTED', 'Refusée'
    COMPLETED = 'COMPLETED', 'Terminée'


class PaymentMethod(models.TextChoices):
    """Méthodes de paiement disponibles."""
    CASH = 'CASH', 'Espèces'
    MTN = 'MTN', 'MTN Mobile Money'
    ORANGE = 'ORANGE', 'Orange Money'


class Booking(models.Model):
    """Modèle représentant une réservation de trajet.
    
    Règles métier critiques :
    - Le client ne doit JAMAIS fournir sa CNI ou ses documents lors d'une réservation.
    - Le système vérifie uniquement que son compte est actif et son profil validé.
    - Le prix unitaire, le montant total et le nombre de places sont contrôlés côté serveur.
    """
    # Parties impliquées
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    trip_offer = models.ForeignKey(
        'trips.TripOffer',
        on_delete=models.CASCADE,
        related_name='bookings'
    )

    # Détails de la réservation
    nombre_places = models.PositiveSmallIntegerField()
    prix_unitaire = models.PositiveIntegerField(help_text='Prix en FCFA')
    montant_total = models.PositiveIntegerField(help_text='Montant total en FCFA')

    # Statuts
    statut = models.CharField(max_length=20, choices=BookingStatus.choices, default=BookingStatus.PENDING)

    # Paiement
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
    payment_status = models.CharField(max_length=20, default='PENDING')  # PENDING, SUCCESS, FAILED
    transaction_reference = models.CharField(max_length=200, blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Réservation'
        verbose_name_plural = 'Réservations'
        ordering = ['-created_at']

    def __str__(self):
        # Représentation lisible d'une réservation
        return f"Réservation({self.client}) pour trajet {self.trip_offer.id} - {self.statut}"

    def save(self, *args, **kwargs):
        """Applique les règles métier avant sauvegarde."""
        # Lors de la création, calculer le montant total côté serveur
        if not self.montant_total:
            self.montant_total = self.prix_unitaire * self.nombre_places
        super().save(*args, **kwargs)

    def is_valid_for_creation(self):
        """Vérifie si la réservation peut être créée.
        
        - Client doit être vérifié
        - Offre ne doit pas être complète
        - Offre ne doit pas être passée
        """
        # Importe ici pour éviter les imports circulaires
        from trips.models import TripStatus
        from datetime import datetime
        
        # Vérifier que le client est vérifié
        if not self.client.can_make_booking():
            return False, "Votre profil doit être vérifié avant de réserver."

        # Vérifier que l'offre existe et a des places
        if self.trip_offer.places_disponibles < self.nombre_places:
            return False, "Pas assez de places disponibles."

        # Vérifier que l'offre n'est pas dans le passé
        if self.trip_offer.date_depart < datetime.now().date():
            return False, "Vous ne pouvez pas réserver un trajet passé."

        # Vérifier que l'offre n'est pas complète
        if self.trip_offer.is_full():
            return False, "Ce trajet est complet."

        return True, "OK"
