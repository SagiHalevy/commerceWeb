from .models import Notification

#everytime page is loaded, notification_count is sent to each of the page's layout and updated "watchlist(x)"
def notification_count(request):
    if request.user.is_authenticated:
        return {'notification_count': Notification.objects.filter(user=request.user, is_read=False).count()}
    return {}