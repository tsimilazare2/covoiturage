from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from bookings.models import Booking
from .forms import TripOfferForm
from .models import TripOffer, TripStatus


@login_required
def publish_trip(request):
    user = request.user
    if not user.is_driver():
        messages.error(request, 'Seuls les chauffeurs peuvent publier des trajets.')
        return redirect('trips:dashboard')
    if not user.is_fully_verified():
        messages.error(request, 'Votre profil chauffeur doit être vérifié avant de publier un trajet.')
        return redirect('trips:dashboard')

    form = TripOfferForm(request.POST or None, user=user)
    if request.method == 'POST' and form.is_valid():
        offer = form.save(commit=False)
        offer.driver = user
        offer.prix_unitaire = offer.route.prix
        offer.places_disponibles = offer.places_totales
        offer.statut = TripStatus.PUBLISHED
        offer.save()
        messages.success(request, 'Trajet publié avec succès.')
        return redirect('trips:dashboard')
    return render(request, 'trips/publish_trip.html', {'form': form})


@login_required
def dashboard(request):
    """Tableau personnel : offres côté chauffeur, réservations/paiements côté passager."""
    if request.user.is_driver():
        offers = TripOffer.objects.filter(driver=request.user).select_related('route').order_by('-date_depart', '-heure_depart')
        profile = getattr(request.user, 'driver_profile', None)
        return render(request, 'trips/dashboard.html', {'offers': offers, 'profile': profile, 'is_driver_dashboard': True})

    bookings = Booking.objects.filter(client=request.user).select_related('trip_offer__route', 'trip_offer__driver', 'payment')
    return render(request, 'trips/dashboard.html', {'bookings': bookings, 'is_driver_dashboard': False})
