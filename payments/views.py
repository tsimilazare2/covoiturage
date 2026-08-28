from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from bookings.models import Booking
from notifications.models import Notification, NotificationType
from .forms import PaymentForm
from .models import Payment, PaymentMethod, PaymentStatus


@login_required
def payment_page(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, client=request.user)
    if hasattr(booking, 'payment') and booking.payment.status == PaymentStatus.SUCCESS:
        messages.info(request, 'Ce paiement a déjà été enregistré.')
        return redirect('bookings:booking_confirmation', booking_id=booking.id)

    form = PaymentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        payment, _ = Payment.objects.get_or_create(
            booking=booking,
            defaults={'amount': booking.montant_total, 'method': form.cleaned_data['method']},
        )
        payment.amount = booking.montant_total
        payment.method = form.cleaned_data['method']
        payment.phone_number = form.cleaned_data.get('phone_number')
        if payment.method == PaymentMethod.CASH:
            success, msg = payment.process_cash_payment()
        elif payment.method == PaymentMethod.MTN:
            success, msg = payment.process_mobile_money_payment()
        else:
            success, msg = payment.process_orange_money_payment()

        if not success:
            messages.error(request, msg)
            return redirect('payments:payment_page', booking_id=booking.id)

        # Une demande Mobile Money reste en attente jusqu'à la confirmation du prestataire.
        if payment.status == PaymentStatus.SUCCESS:
            booking.statut = 'CONFIRMED'
        booking.payment_status = payment.status
        booking.transaction_reference = payment.transaction_reference
        booking.save()
        if payment.status == PaymentStatus.SUCCESS:
            Notification.objects.create(
                recipient=booking.trip_offer.driver,
                title='Nouvelle réservation confirmée',
                message=f'{request.user.full_name() or request.user.username} a confirmé une réservation pour votre trajet.',
                type=NotificationType.BOOKING_CONFIRMED,
            )
        messages.success(request, msg)
        return redirect('bookings:booking_confirmation', booking_id=booking.id)
    return render(request, 'payments/payment_page.html', {'form': form, 'booking': booking})
