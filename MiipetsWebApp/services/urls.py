from django.urls import path
from . import views as listing_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('all-listing/', listing_views.view_all_services, name='services-all'),
    path('services/<str:type>', listing_views.view_services, name='services'),
    path('single-listing/<int:service_id>', listing_views.view_single_services, name='services-single'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
