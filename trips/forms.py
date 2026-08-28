from django import forms
from .models import TripOffer, TripStatus
from routes.models import Route
from vehicles.models import Vehicle


class TripOfferForm(forms.ModelForm):
    class Meta:
        model = TripOffer
        fields = ['route', 'vehicle', 'date_depart', 'heure_depart', 'places_totales']
        widgets = {
            'route': forms.Select(attrs={'class': 'w-full rounded-lg border border-gray-300 p-2.5'}),
            'vehicle': forms.Select(attrs={'class': 'w-full rounded-lg border border-gray-300 p-2.5'}),
            'date_depart': forms.DateInput(attrs={'type': 'date', 'class': 'w-full rounded-lg border border-gray-300 p-2.5'}),
            'heure_depart': forms.TimeInput(attrs={'type': 'time', 'class': 'w-full rounded-lg border border-gray-300 p-2.5'}),
            'places_totales': forms.NumberInput(attrs={'min': 1, 'class': 'w-full rounded-lg border border-gray-300 p-2.5'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # Only show active routes
        self.fields['route'].queryset = Route.objects.filter(active=True)
        # If user provided, limit vehicles to user's vehicles
        if user is not None:
            self.fields['vehicle'].queryset = Vehicle.objects.filter(owner=user)
        else:
            self.fields['vehicle'].queryset = Vehicle.objects.none()

    def clean(self):
        cleaned = super().clean()
        route = cleaned.get('route')
        if route:
            # ensure prix_unitaire will be taken from route
            cleaned['prix_unitaire'] = route.prix
        return cleaned

    # Commentaires en français :
    # Le formulaire affiche uniquement les itinéraires actifs et les véhicules appartenant
    # au chauffeur connecté (si présents). Le prix n'est pas saisi par le chauffeur ;
    # il sera calculé côté serveur à partir de la `Route` sélectionnée.
