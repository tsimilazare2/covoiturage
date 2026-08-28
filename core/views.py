from django.shortcuts import render


def home(request):
    """Vue d'accueil — affiche la page d'accueil avec call to action pour s'inscrire/chercher un trajet."""
    context = {
        'title': 'Accueil — Maroua Covoit',
        'description': 'La plateforme de covoiturage sécurisée pour Maroua',
    }
    return render(request, 'core/home.html', context)
