import datetime
from django.conf import settings
from django.db import models


class Vehicle(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vehicles')
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=50, blank=True, null=True)
    year = models.PositiveSmallIntegerField(blank=True, null=True)
    plate_number = models.CharField(max_length=50)
    seats = models.PositiveSmallIntegerField(default=4)
    photo = models.ImageField(upload_to='vehicles/photos/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Véhicule'
        verbose_name_plural = 'Véhicules'

    def __str__(self):
        # Affichage lisible du véhicule
        return f"{self.make} {self.model} ({self.plate_number})"

    def is_fully_verified(self):
        """Vérifie si le véhicule et ses documents sont marqués comme vérifiés."""
        return self.is_verified and all(doc.expiry_date is None or doc.expiry_date >= datetime.date.today() for doc in self.documents.all())


class VehicleDocument(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=100)
    number = models.CharField(max_length=100, blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    file = models.FileField(upload_to='vehicles/documents/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Document de véhicule'
        verbose_name_plural = 'Documents de véhicule'

    def __str__(self):
        # Représentation lisible du document du véhicule
        return f"{self.vehicle} - {self.doc_type}"
