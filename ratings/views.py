from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render

from bookings.models import Booking, BookingStatus
from notifications.models import Notification, NotificationType
from .forms import RatingForm
from .models import Rating


@login_required
def rate_driver(request, booking_id):
    """Permet à un passager de noter son chauffeur après un trajet terminé."""
    booking = get_object_or_404(Booking, id=booking_id, client=request.user)
    if booking.statut != BookingStatus.COMPLETED:
        messages.error(request, 'Vous pourrez évaluer le chauffeur une fois le trajet terminé.')
        return redirect('trips:dashboard')
    if hasattr(booking, 'rating'):
        messages.info(request, 'Vous avez déjà évalué ce trajet.')
        return redirect('trips:dashboard')

    form = RatingForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        rating = form.save(commit=False)
        rating.client = request.user
        rating.driver = booking.trip_offer.driver
        rating.booking = booking
        rating.save()
        Notification.objects.create(
            recipient=rating.driver,
            title='Nouvelle évaluation reçue',
            message=f'{request.user.full_name() or request.user.username} vous a attribué {rating.score}/5.',
            type=NotificationType.NEW_RATING,
        )
        messages.success(request, 'Merci, votre évaluation a été enregistrée.')
        return redirect('trips:dashboard')
    return render(request, 'ratings/rate_driver.html', {'form': form, 'booking': booking})


@login_required
def ratings_received(request):
    """Liste les évaluations reçues par le chauffeur connecté."""
    if not request.user.is_driver():
        messages.error(request, 'Cette page est réservée aux chauffeurs.')
        return redirect('trips:dashboard')
    ratings = Rating.objects.filter(driver=request.user).select_related('client', 'booking__trip_offer__route')
    average = ratings.aggregate(average=Avg('score'))['average'] or 0
    return render(request, 'ratings/ratings_received.html', {'ratings': ratings, 'average': round(average, 1)})
