from django.urls import path
from . import views as review_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('review-pet-service/<int:booking_id>', review_views.add_review, name='reviews-review-service'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
