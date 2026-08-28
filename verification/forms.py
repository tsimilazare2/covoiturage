from django import forms

from vehicles.models import Vehicle
from .models import DriverProfile


FIELD_CLASS = 'w-full rounded-lg border border-gray-300 px-3 py-2.5 focus:border-green-600 focus:ring-green-600'


class DriverProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ('cni_number', 'cni_front', 'cni_back', 'cni_expiry', 'license_number', 'license_category', 'license_expiry', 'license_image'):
            self.fields[name].required = True

    class Meta:
        model = DriverProfile
        fields = ['cni_number', 'cni_front', 'cni_back', 'cni_expiry', 'license_number', 'license_category', 'license_expiry', 'license_image']
        labels = {
            'cni_number': 'Numéro de CNI', 'cni_front': 'Recto de la CNI', 'cni_back': 'Verso de la CNI',
            'cni_expiry': "Date d'expiration de la CNI", 'license_number': 'Numéro de permis',
            'license_category': 'Catégorie de permis', 'license_expiry': "Date d'expiration du permis", 'license_image': 'Photo du permis',
        }
        widgets = {
            'cni_number': forms.TextInput(attrs={'class': FIELD_CLASS}), 'cni_expiry': forms.DateInput(attrs={'class': FIELD_CLASS, 'type': 'date'}),
            'license_number': forms.TextInput(attrs={'class': FIELD_CLASS}), 'license_category': forms.TextInput(attrs={'class': FIELD_CLASS, 'placeholder': 'Ex. B'}),
            'license_expiry': forms.DateInput(attrs={'class': FIELD_CLASS, 'type': 'date'}),
        }


class VehicleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ('make', 'model', 'plate_number', 'seats'):
            self.fields[name].required = True

    class Meta:
        model = Vehicle
        fields = ['make', 'model', 'color', 'year', 'plate_number', 'seats', 'photo']
        labels = {'make': 'Marque', 'model': 'Modèle', 'color': 'Couleur', 'year': 'Année', 'plate_number': "Immatriculation", 'seats': 'Nombre de places', 'photo': 'Photo du véhicule'}
        widgets = {
            'make': forms.TextInput(attrs={'class': FIELD_CLASS, 'placeholder': 'Toyota'}), 'model': forms.TextInput(attrs={'class': FIELD_CLASS, 'placeholder': 'Corolla'}),
            'color': forms.TextInput(attrs={'class': FIELD_CLASS}), 'year': forms.NumberInput(attrs={'class': FIELD_CLASS, 'min': 1980}),
            'plate_number': forms.TextInput(attrs={'class': FIELD_CLASS, 'placeholder': 'Ex. CE 123 AB'}), 'seats': forms.NumberInput(attrs={'class': FIELD_CLASS, 'min': 1, 'max': 20}),
        }
