from django.conf import settings
from django.db import models


class PaymentStatus(models.TextChoices):
    """Statuts possibles d'un paiement."""
    PENDING = 'PENDING', 'En attente'
    SUCCESS = 'SUCCESS', 'Réussi'
    FAILED = 'FAILED', 'Échoué'
    CANCELLED = 'CANCELLED', 'Annulé'


class PaymentMethod(models.TextChoices):
    """Méthodes de paiement disponibles."""
    CASH = 'CASH', 'Espèces'
    MTN = 'MTN', 'MTN Mobile Money'
    ORANGE = 'ORANGE', 'Orange Money'


class Payment(models.Model):
    """Modèle représentant un paiement.
    
    Règles métier critiques :
    - NE JAMAIS demander ou stocker un PIN Mobile Money.
    - NE JAMAIS stocker de données bancaires sensibles.
    - L'architecture est extensible pour intégrer une vraie API ultérieurement.
    - Pour Mobile Money / Orange Money, seul le numéro de téléphone est stocké.
    """
    # Lien avec la réservation
    booking = models.OneToOneField(
        'bookings.Booking',
        on_delete=models.CASCADE,
        related_name='payment'
    )

    # Détails du paiement
    amount = models.PositiveIntegerField(help_text='Montant en FCFA')
    method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)

    # Pour Mobile Money / Orange Money
    phone_number = models.CharField(max_length=20, blank=True, null=True, help_text='Numéro de téléphone pour paiement Mobile Money/Orange Money')

    # Référence de transaction
    transaction_reference = models.CharField(max_length=200, blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Paiement'
        verbose_name_plural = 'Paiements'
        ordering = ['-created_at']

    def __str__(self):
        # Représentation lisible d'un paiement
        return f"Paiement({self.booking.client}) - {self.amount} FCFA - {self.method} - {self.status}"

    def process_cash_payment(self):
        """Simule le traitement d'un paiement en espèces."""
        self.status = PaymentStatus.SUCCESS
        self.transaction_reference = f"CASH-{self.booking.id}"
        self.save()
        return True, "Paiement en espèces enregistré."

    def process_mobile_money_payment(self):
        """Simule la demande d'un paiement Mobile Money.
        
        Pour le MVP, marquer comme PENDING en attente de confirmation.
        Architecture prête pour intégrer une vraie API.
        """
        if not self.phone_number:
            return False, "Numéro de téléphone requis."
        
        # Simulation : marquer en attente
        self.status = PaymentStatus.PENDING
        self.transaction_reference = f"MM-{self.booking.id}"
        self.save()
        
        # Dans une vraie implémentation, faire appel à l'API du prestataire
        # from payments.services import MobileMoneyService
        # service = MobileMoneyService()
        # success = service.initiate_payment(...)
        
        return True, f"Demande de paiement envoyée au {self.phone_number}. Veuillez confirmer sur votre téléphone."

    def process_orange_money_payment(self):
        """Simule la demande d'un paiement Orange Money.
        
        Pour le MVP, marquer comme PENDING en attente de confirmation.
        """
        if not self.phone_number:
            return False, "Numéro de téléphone requis."
        
        self.status = PaymentStatus.PENDING
        self.transaction_reference = f"OM-{self.booking.id}"
        self.save()
        
        # Dans une vraie implémentation, faire appel à l'API d'Orange
        return True, f"Demande de paiement envoyée au {self.phone_number}. Veuillez confirmer sur votre téléphone."
