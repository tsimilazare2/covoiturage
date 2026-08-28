from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from .models import Notification


class NotificationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='notifie', password='motdepasse123')
        self.notification = Notification.objects.create(recipient=self.user, title='Information', message='Un message de test.')

    def test_unread_count_and_mark_as_read(self):
        self.assertEqual(Notification.unread_count(self.user), 1)
        self.client.force_login(self.user)
        response = self.client.get(reverse('notifications:mark_as_read', args=[self.notification.pk]))
        self.assertRedirects(response, reverse('notifications:list'))
        self.assertEqual(Notification.unread_count(self.user), 0)

    def test_notifications_list_is_protected(self):
        response = self.client.get(reverse('notifications:list'))
        self.assertEqual(response.status_code, 302)
