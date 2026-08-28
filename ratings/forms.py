from django import forms

from .models import Rating


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['score', 'commentaire']
        labels = {'score': 'Votre note', 'commentaire': 'Commentaire (facultatif)'}
        widgets = {
            'score': forms.Select(choices=[(i, f'{i} étoile' + ('s' if i > 1 else '')) for i in range(1, 6)], attrs={'class': 'form-control'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Partagez votre expérience…'}),
        }
