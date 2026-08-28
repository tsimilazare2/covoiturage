from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()
INPUT_CLASS = 'w-full rounded-lg border border-gray-300 py-2.5 pl-10 pr-3 focus:border-green-600 focus:ring-green-600'


class SignUpForm(forms.ModelForm):
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(attrs={'class': INPUT_CLASS}), min_length=8)
    password2 = forms.CharField(label='Confirmer le mot de passe', widget=forms.PasswordInput(attrs={'class': INPUT_CLASS}), min_length=8)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'role', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'ex. aminatou'}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASS, 'placeholder': 'nom@exemple.com'}),
            'first_name': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Votre prénom'}),
            'last_name': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Votre nom'}),
            'phone': forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': '+237 6XX XXX XXX'}),
            'role': forms.Select(attrs={'class': INPUT_CLASS}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') and cleaned.get('password2') and cleaned['password'] != cleaned['password2']:
            raise forms.ValidationError('Les mots de passe ne correspondent pas.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'placeholder': "Votre nom d'utilisateur"}))
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(attrs={'class': INPUT_CLASS, 'placeholder': 'Votre mot de passe'}))


class AccountSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'profile_photo']
        labels = {'first_name': 'Prénom', 'last_name': 'Nom', 'email': 'Adresse e-mail', 'phone': 'Téléphone', 'profile_photo': 'Photo de profil'}
        widgets = {
            'first_name': forms.TextInput(attrs={'class': INPUT_CLASS}), 'last_name': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASS}), 'phone': forms.TextInput(attrs={'class': INPUT_CLASS}),
        }


class FrenchPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Mot de passe actuel', widget=forms.PasswordInput(attrs={'class': INPUT_CLASS}))
    new_password1 = forms.CharField(label='Nouveau mot de passe', widget=forms.PasswordInput(attrs={'class': INPUT_CLASS}))
    new_password2 = forms.CharField(label='Confirmer le nouveau mot de passe', widget=forms.PasswordInput(attrs={'class': INPUT_CLASS}))
