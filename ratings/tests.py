from datetime import date, time, timedelta

from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from bookings.models import Booking, BookingStatus
from routes.models import Route
from trips.models import TripOffer, TripStatus
from vehicles.models import Vehicle
from .models import Rating


class RatingTests(TestCase):
    def setUp(self):
        self.driver = User.objects.create_user(username='chauffeur-note', password='motdepasse123', role=User.ROLE_DRIVER)
        self.passenger = User.objects.create_user(username='passager-note', password='motdepasse123', role=User.ROLE_PASSENGER)
        route = Route.objects.create(name='Note', point_depart='Maroua', destination='Bogo', prix=600)
        vehicle = Vehicle.objects.create(owner=self.driver, make='Toyota', model='Yaris', plate_number='NO123')
        trip = TripOffer.objects.create(driver=self.driver, route=route, vehicle=vehicle, date_depart=date.today() + timedelta(days=1), heure_depart=time(8), places_totales=4, places_disponibles=3, prix_unitaire=600, statut=TripStatus.COMPLETED)
        self.booking = Booking.objects.create(client=self.passenger, trip_offer=trip, nombre_places=1, prix_unitaire=600, montant_total=600, statut=BookingStatus.COMPLETED)

    def test_passenger_can_rate_completed_trip_and_driver_is_notified(self):
        self.client.force_login(self.passenger)
        response = self.client.post(reverse('ratings:rate_driver', args=[self.booking.id]), {'score': 5, 'commentaire': 'Très bon trajet.'})
        self.assertRedirects(response, reverse('trips:dashboard'))
        self.assertEqual(Rating.objects.get().score, 5)
        self.assertEqual(self.driver.notifications.count(), 1)

    def test_rating_is_refused_before_trip_completion(self):
        self.booking.statut = BookingStatus.CONFIRMED
        self.booking.save()
        self.client.force_login(self.passenger)
        self.client.post(reverse('ratings:rate_driver', args=[self.booking.id]), {'score': 4})
        self.assertEqual(Rating.objects.count(), 0)
