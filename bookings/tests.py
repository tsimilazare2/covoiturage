from datetime import date, time, timedelta

from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from routes.models import Route
from trips.models import TripOffer, TripStatus
from vehicles.models import Vehicle
from verification.models import ClientVerification, VerificationStatus


class BookingTests(TestCase):
    def setUp(self):
        self.driver = User.objects.create_user(username='chauffeur', password='motdepasse123', role=User.ROLE_DRIVER)
        self.passenger = User.objects.create_user(username='passager', password='motdepasse123', role=User.ROLE_PASSENGER)
        ClientVerification.objects.create(user=self.passenger, status=VerificationStatus.VALIDE)
        route = Route.objects.create(name='Maroua-Domayo', point_depart='Maroua', destination='Domayo', prix=500)
        vehicle = Vehicle.objects.create(owner=self.driver, make='Toyota', model='Corolla', plate_number='LT123AB')
        self.trip = TripOffer.objects.create(driver=self.driver, route=route, vehicle=vehicle, date_depart=date.today() + timedelta(days=2), heure_depart=time(9), places_totales=3, places_disponibles=3, prix_unitaire=500, statut=TripStatus.PUBLISHED)

    def test_verified_passenger_can_book_and_places_are_reduced(self):
        self.client.force_login(self.passenger)
        response = self.client.post(reverse('bookings:create_booking', args=[self.trip.id]), {'nombre_places': 2, 'payment_method': 'CASH'})
        self.assertRedirects(response, reverse('payments:payment_page', args=[1]))
        self.trip.refresh_from_db()
        self.assertEqual(self.trip.places_disponibles, 1)

    def test_booking_cannot_exceed_available_places(self):
        self.client.force_login(self.passenger)
        response = self.client.post(reverse('bookings:create_booking', args=[self.trip.id]), {'nombre_places': 4, 'payment_method': 'CASH'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.trip.bookings.count(), 0)
