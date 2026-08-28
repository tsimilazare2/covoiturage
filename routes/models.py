from django.db import models


class Route(models.Model):
    name = models.CharField(max_length=200)
    point_depart = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    distance_km = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    duree_estimee = models.DurationField(blank=True, null=True)
    prix = models.PositiveIntegerField(help_text='Prix en FCFA')
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Route'
        verbose_name_plural = 'Routes'
        ordering = ['-created_at']

    def __str__(self):
        # Représentation lisible d'un itinéraire, affichée en admin et dans les listes
        return f"{self.point_depart} → {self.destination} ({self.prix} FCFA)"

    def price_display(self):
        """Retourne une représentation formatée du prix (ex: '500 FCFA')."""
        return f"{self.prix} FCFA"
