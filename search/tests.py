from datetime import date, time, timedelta

from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from routes.models import Route
from trips.models import TripOffer, TripStatus
from vehicles.models import Vehicle


class SearchTests(TestCase):
    def setUp(self):
        driver = User.objects.create_user(username='driver', password='motdepasse123', role=User.ROLE_DRIVER, is_verified=True)
        route = Route.objects.create(name='Maroua-Mokolo', point_depart='Maroua', destination='Mokolo', prix=1200)
        vehicle = Vehicle.objects.create(owner=driver, make='Nissan', model='Sunny', plate_number='EN123')
        self.trip = TripOffer.objects.create(driver=driver, route=route, vehicle=vehicle, date_depart=date.today() + timedelta(days=1), heure_depart=time(7), places_totales=4, places_disponibles=2, prix_unitaire=1200, statut=TripStatus.PUBLISHED)

    def test_search_is_public_and_filters_departure_destination_price_and_places(self):
        response = self.client.get(reverse('search:search'), {'point_depart': 'maroua', 'destination': 'mok', 'prix_max': 1300, 'nombre_places': 2, 'driver_verifie': 'on'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Maroua')
        response = self.client.get(reverse('search:search'), {'prix_max': 1000})
        self.assertNotContains(response, 'Nissan Sunny')
