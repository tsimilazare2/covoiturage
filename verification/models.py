from django.conf import settings
from django.db import models


class VerificationStatus(models.TextChoices):
    NON_SOUMIS = 'NON_SOUMIS', 'Non soumis'
    EN_ATTENTE = 'EN_ATTENTE', 'En attente'
    VALIDE = 'VALIDE', 'Valide'
    REFUSE = 'REFUSE', 'Refusé'
    EXPIRE = 'EXPIRE', 'Expiré'


class ClientVerification(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='client_verification')
    cni_number = models.CharField(max_length=100, blank=True, null=True)
    cni_front = models.ImageField(upload_to='verifications/clients/', blank=True, null=True)
    cni_back = models.ImageField(upload_to='verifications/clients/', blank=True, null=True)
    expiry_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=VerificationStatus.choices, default=VerificationStatus.NON_SOUMIS)
    submitted_at = models.DateTimeField(blank=True, null=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Vérification passager'
        verbose_name_plural = 'Vérifications passagers'

    def __str__(self):
        # Représentation lisible en admin
        return f"Vérification({self.user}) - {self.status}"


class DriverProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='driver_profile')
    cni_number = models.CharField(max_length=100, blank=True, null=True)
    cni_front = models.ImageField(upload_to='verifications/drivers/', blank=True, null=True)
    cni_back = models.ImageField(upload_to='verifications/drivers/', blank=True, null=True)
    cni_expiry = models.DateField(blank=True, null=True)

    license_number = models.CharField(max_length=100, blank=True, null=True)
    license_category = models.CharField(max_length=50, blank=True, null=True)
    license_expiry = models.DateField(blank=True, null=True)
    license_image = models.ImageField(upload_to='verifications/drivers/licenses/', blank=True, null=True)

    status = models.CharField(max_length=20, choices=VerificationStatus.choices, default=VerificationStatus.NON_SOUMIS)
    submitted_at = models.DateTimeField(blank=True, null=True)
    reviewed_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Profil chauffeur'
        verbose_name_plural = 'Profils chauffeurs'

    def __str__(self):
        # Représentation lisible en admin
        return f"ProfilChauffeur({self.user}) - {self.status}"

    def is_valid(self):
        """Renvoie True si le profil du chauffeur est validé par l'admin."""
        return self.status == VerificationStatus.VALIDE
