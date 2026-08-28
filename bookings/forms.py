from django import forms
from .models import Booking, PaymentMethod


class BookingForm(forms.ModelForm):
    """Formulaire de création de réservation.
    
    Le formulaire n'inclut que :
    - nombre_places
    - payment_method
    
    Les autres champs (prix, montant total, client, etc.) sont complétés côté serveur.
    """
    class Meta:
        model = Booking
        fields = ['nombre_places', 'payment_method']
        widgets = {
            'nombre_places': forms.NumberInput(attrs={'min': 1, 'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        trip_offer = kwargs.pop('trip_offer', None)
        super().__init__(*args, **kwargs)
        self.trip_offer = trip_offer

    def clean(self):
        cleaned = super().clean()
        nombre_places = cleaned.get('nombre_places')

        # Vérifier que le nombre de places est valide
        if nombre_places and self.trip_offer:
            if nombre_places > self.trip_offer.places_disponibles:
                raise forms.ValidationError(f"Il y a seulement {self.trip_offer.places_disponibles} places disponibles.")

        return cleaned
