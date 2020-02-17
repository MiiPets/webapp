from django.urls import path
from . import views as mass_emails_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('notify-sitters-add-service', 
         mass_emails_views.send_sitter_notification_add_services,
         name='mass-emails-notify-sitters-add-service'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
