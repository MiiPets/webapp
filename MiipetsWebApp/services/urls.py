from django.urls import path
from . import views as service_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('all-services/', service_views.view_all_services, name='services-all'),
    path('services/<str:type>', service_views.view_services, name='services'),
    path('single-service/<int:service_id>', service_views.view_single_service, name='services-single'),
    path('ajax/load-timeslots/<int:service_id>', service_views.load_timeslots, name='ajax_load_time'),
    path('booking_confirmation/<int:service_id>/<int:booking_id>', service_views.booking_confirmation, name='services-booking-confirmation'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
