from .models import Notification


def notifications_unread_count(request):
    """Expose le nombre de notifications non lues dans la navigation."""
    if not request.user.is_authenticated:
        return {'notifications_unread_count': 0}
    return {'notifications_unread_count': Notification.unread_count(request.user)}
