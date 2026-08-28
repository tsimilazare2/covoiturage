from django import forms
from .models import Payment, PaymentMethod


class PaymentForm(forms.ModelForm):
    """Formulaire de paiement pour une réservation.
    
    Affiche les options de paiement (CASH, MTN, ORANGE).
    Si MTN ou ORANGE, demande le numéro de téléphone.
    """
    class Meta:
        model = Payment
        fields = ['method', 'phone_number']
        widgets = {
            'method': forms.RadioSelect(choices=PaymentMethod.choices),
            'phone_number': forms.TextInput(attrs={'placeholder': '+237 6XX XXX XXX', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone_number'].required = False

    def clean(self):
        cleaned = super().clean()
        method = cleaned.get('method')
        phone_number = cleaned.get('phone_number')

        # Si Mobile Money ou Orange Money, le numéro est requis
        if method in [PaymentMethod.MTN, PaymentMethod.ORANGE] and not phone_number:
            raise forms.ValidationError(f"Le numéro de téléphone est requis pour {method}.")

        return cleaned
