from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from .forms import BookingForm
from .models import Booking


@login_required
def create_booking(request, trip_id):
    """Crée une réservation de passager et protège le stock de places."""
    from trips.models import TripOffer

    user = request.user
    if not user.is_passenger():
        messages.error(request, 'Seuls les passagers peuvent réserver des trajets.')
        return redirect('trips:dashboard')
    if not user.can_make_booking():
        messages.error(request, 'Votre profil doit être vérifié avant de réserver un trajet.')
        return redirect('trips:dashboard')

    trip_offer = get_object_or_404(TripOffer, id=trip_id)
    form = BookingForm(request.POST or None, trip_offer=trip_offer)
    if request.method == 'POST' and form.is_valid():
        booking = form.save(commit=False)
        booking.client = user
        booking.trip_offer = trip_offer
        booking.prix_unitaire = trip_offer.prix_unitaire
        booking.montant_total = booking.prix_unitaire * booking.nombre_places
        is_valid, error_msg = booking.is_valid_for_creation()
        if not is_valid:
            messages.error(request, error_msg)
            return redirect('search:search')

        with transaction.atomic():
            trip_offer.refresh_from_db()
            if trip_offer.places_disponibles < booking.nombre_places:
                messages.error(request, 'Les places viennent d’être réservées par un autre passager.')
                return redirect('search:search')
            booking.save()
            trip_offer.places_disponibles -= booking.nombre_places
            if trip_offer.places_disponibles == 0:
                trip_offer.statut = 'FULL'
            trip_offer.save()

        messages.success(request, 'Réservation créée avec succès. Procédez au paiement.')
        return redirect('payments:payment_page', booking_id=booking.id)
    return render(request, 'bookings/create_booking.html', {'form': form, 'trip_offer': trip_offer})


@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, client=request.user)
    return render(request, 'bookings/booking_confirmation.html', {'booking': booking})
