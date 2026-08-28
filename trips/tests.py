from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from routes.models import Route
from vehicles.models import Vehicle
from verification.models import DriverProfile, VerificationStatus


class TripPublishTests(TestCase):
    def setUp(self):
        # Crée un utilisateur chauffeur
        self.driver = User.objects.create_user(username='chauff', password='pass1234', role=User.ROLE_DRIVER)
        # Crée et valide le DriverProfile
        DriverProfile.objects.create(user=self.driver, status=VerificationStatus.VALIDE)

        # Crée un véhicule pour le chauffeur
        self.vehicle = Vehicle.objects.create(owner=self.driver, make='Toyota', model='Corolla', plate_number='AB1234', seats=4)

        # Crée un itinéraire
        self.route = Route.objects.create(name='Maroua-Domayo', point_depart='Maroua', destination='Domayo', prix=500)

        # Client pour faire les requêtes
        self.client = Client()

    def test_driver_can_publish_trip_and_price_is_from_route(self):
        # Connexion
        self.client.login(username='chauff', password='pass1234')

        url = reverse('trips:publish')
        resp = self.client.post(url, data={
            'route': self.route.id,
            'vehicle': self.vehicle.id,
            'date_depart': timezone.now().date(),
            'heure_depart': '12:00',
            'places_totales': 3,
        }, follow=True)

        self.assertEqual(resp.status_code, 200)
        # Vérifier qu'une offre a été créée et que le prix provient de la route
        from trips.models import TripOffer
        offer = TripOffer.objects.filter(driver=self.driver).first()
        self.assertIsNotNone(offer)
        self.assertEqual(offer.prix_unitaire, self.route.prix)
        self.assertEqual(offer.statut, 'PUBLISHED')

    def test_non_driver_cannot_access_publish(self):
        # Crée un utilisateur passager
        user = User.objects.create_user(username='client', password='pwd', role=User.ROLE_PASSENGER)
        self.client.login(username='client', password='pwd')
        url = reverse('trips:publish')
        resp = self.client.get(url, follow=True)
        # Doit être redirigé (erreur message) et ne pas permettre l'accès
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Seuls les chauffeurs peuvent publier des trajets', status_code=200)