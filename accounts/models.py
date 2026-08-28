from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Modèle utilisateur personnalisé pour la plateforme de covoiturage Maroua.
    
    Rôles disponibles :
    - DRIVER: Chauffeur (propose des trajets)
    - PASSENGER: Passager (réserve des trajets)
    """
    ROLE_DRIVER = 'DRIVER'
    ROLE_PASSENGER = 'PASSENGER'

    ROLE_CHOICES = [
        (ROLE_DRIVER, 'Chauffeur'),
        (ROLE_PASSENGER, 'Passager'),
    ]

    phone = models.CharField(max_length=30, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ROLE_PASSENGER)
    profile_photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        ordering = ['-date_joined']

    def full_name(self):
        """Retourne le nom complet de l'utilisateur (prénom + nom).

        Exemple: "Jean Dupont". Si l'un des champs est vide, la méthode
        renvoie la partie disponible.
        """
        return f"{self.first_name} {self.last_name}".strip()

    def is_driver(self):
        """Indique si l'utilisateur a le rôle `DRIVER`."""
        return self.role == self.ROLE_DRIVER

    def is_passenger(self):
        """Indique si l'utilisateur a le rôle `PASSENGER`."""
        return self.role == self.ROLE_PASSENGER

    def is_fully_verified(self):
        """Indique si le chauffeur est entièrement vérifié.

        - Ne s'applique qu'aux utilisateurs de type chauffeur.
        - Vérifie l'existence d'un `DriverProfile` et que son `status` vaut `VALIDE`.
        """
        if not self.is_driver():
            return False
        try:
            profile = self.driver_profile
        except Exception:
            return False
        return getattr(profile, 'status', None) == 'VALIDE'

    def can_make_booking(self):
        """Indique si le client peut effectuer une réservation.

        Conditions principales :
        - l'utilisateur est un `PASSENGER`;
        - un `ClientVerification` existe et son `status` vaut `VALIDE`.
        """
        if not self.is_passenger():
            return False
        try:
            cv = self.client_verification
        except Exception:
            return False
        return getattr(cv, 'status', None) == 'VALIDE'
