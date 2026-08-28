from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Rating(models.Model):
    """Modèle d'évaluation d'un trajet par un client.
    
    L'évaluation est donnée après la fin du trajet et permet aux autres clients
    de voter sur la qualité du service du chauffeur.
    """
    # Parties impliquées
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ratings_given'
    )
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ratings_received'
    )
    booking = models.OneToOneField(
        'bookings.Booking',
        on_delete=models.CASCADE,
        related_name='rating'
    )

    # Évaluation
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Note de 1 à 5 étoiles'
    )
    commentaire = models.TextField(blank=True, null=True, max_length=500)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Évaluation'
        verbose_name_plural = 'Évaluations'
        ordering = ['-created_at']
        unique_together = ('client', 'booking')  # Un client ne peut noter qu'une fois par trajet

    def __str__(self):
        # Représentation lisible d'une évaluation
        return f"Note({self.driver}) - {self.score}★ par {self.client}"

    @staticmethod
    def average_driver_rating(driver):
        """Calcule la note moyenne du chauffeur."""
        from django.db.models import Avg
        avg = Rating.objects.filter(driver=driver).aggregate(Avg('score'))['score__avg']
        return round(avg, 1) if avg else 0
