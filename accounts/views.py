from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import AccountSettingsForm, FrenchPasswordChangeForm, SignUpForm, LoginForm


def signup(request):
    """Vue d'inscription pour les nouveaux utilisateurs."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Compte créé avec succès! Connectez-vous pour continuer.')
            return redirect('accounts:login')
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """Vue de connexion."""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                # Rediriger vers la page suivante (next parameter) ou l'accueil
                next_url = request.GET.get('next', 'core:home')
                return redirect(next_url)
            else:
                messages.error(request, 'Nom d\'utilisateur ou mot de passe invalide.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """Vue de déconnexion."""
    logout(request)
    messages.success(request, 'Vous êtes bien déconnecté.')
    return redirect('core:home')


@login_required
def settings_view(request):
    profile_form = AccountSettingsForm(request.POST or None, request.FILES or None, instance=request.user, prefix='profile')
    password_form = FrenchPasswordChangeForm(request.user, request.POST or None, prefix='password')
    if request.method == 'POST':
        if 'save_profile' in request.POST and profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Vos paramètres ont été mis à jour.')
            return redirect('accounts:settings')
        if 'change_password' in request.POST and password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Votre mot de passe a été modifié.')
            return redirect('accounts:settings')
    return render(request, 'accounts/settings.html', {'profile_form': profile_form, 'password_form': password_form})
