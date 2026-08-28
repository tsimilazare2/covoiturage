from datetime import date, time, timedelta

from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from bookings.models import Booking, BookingStatus
from routes.models import Route
from trips.models import TripOffer, TripStatus
from vehicles.models import Vehicle
from .models import Payment, PaymentStatus


class PaymentTests(TestCase):
    def setUp(self):
        driver = User.objects.create_user(username='conducteur', password='motdepasse123', role=User.ROLE_DRIVER)
        self.passenger = User.objects.create_user(username='voyageur', password='motdepasse123', role=User.ROLE_PASSENGER)
        route = Route.objects.create(name='Test', point_depart='Maroua', destination='Salak', prix=750)
        vehicle = Vehicle.objects.create(owner=driver, make='Kia', model='Rio', plate_number='CE001')
        trip = TripOffer.objects.create(driver=driver, route=route, vehicle=vehicle, date_depart=date.today() + timedelta(days=2), heure_depart=time(8), places_totales=4, places_disponibles=3, prix_unitaire=750, statut=TripStatus.PUBLISHED)
        self.booking = Booking.objects.create(client=self.passenger, trip_offer=trip, nombre_places=2, prix_unitaire=750, montant_total=1500)

    def test_cash_payment_confirms_booking_once(self):
        self.client.force_login(self.passenger)
        url = reverse('payments:payment_page', args=[self.booking.id])
        response = self.client.post(url, {'method': 'CASH', 'phone_number': ''})
        self.assertRedirects(response, reverse('bookings:booking_confirmation', args=[self.booking.id]))
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.statut, BookingStatus.CONFIRMED)
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(self.booking.payment.status, PaymentStatus.SUCCESS)
        self.client.post(url, {'method': 'CASH', 'phone_number': ''})
        self.assertEqual(Payment.objects.count(), 1)
