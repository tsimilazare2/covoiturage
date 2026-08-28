from django.conf import settings
from django.db import models


class NotificationType(models.TextChoices):
    """Types de notifications possibles."""
    ACCOUNT_VERIFIED = 'ACCOUNT_VERIFIED', 'Compte vérifié'
    BOOKING_CONFIRMED = 'BOOKING_CONFIRMED', 'Réservation confirmée'
    TRIP_STARTING = 'TRIP_STARTING', 'Trajet commençant bientôt'
    BOOKING_CANCELLED = 'BOOKING_CANCELLED', 'Réservation annulée'
    DOCUMENT_EXPIRED = 'DOCUMENT_EXPIRED', 'Document expiré'
    NEW_RATING = 'NEW_RATING', 'Nouvelle évaluation reçue'
    PAYMENT_RECEIVED = 'PAYMENT_RECEIVED', 'Paiement reçu'
    OTHER = 'OTHER', 'Autre'


class Notification(models.Model):
    """Modèle représentant une notification interne pour un utilisateur.
    
    Les notifications permettent de communiquer avec les utilisateurs
    sans dépendre d'email ou de SMS.
    """
    # Destinataire de la notification
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    # Contenu de la notification
    title = models.CharField(max_length=150)
    message = models.TextField()
    type = models.CharField(max_length=20, choices=NotificationType.choices, default=NotificationType.OTHER)

    # État
    is_read = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ['-created_at']

    def __str__(self):
        # Représentation lisible d'une notification
        return f"Notification({self.recipient}) - {self.title}"

    def mark_as_read(self):
        """Marque la notification comme lue."""
        self.is_read = True
        self.save()

    @staticmethod
    def unread_count(user):
        """Compte le nombre de notifications non lues pour un utilisateur."""
        return Notification.objects.filter(recipient=user, is_read=False).count()
