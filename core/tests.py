# Tests pour l'app core
from django.test import TestCase


class HomePageTests(TestCase):
    def test_home_page_loads(self):
        """Teste que la page d'accueil se charge correctement."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/home.html')
