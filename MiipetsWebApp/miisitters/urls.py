from django.urls import path
from . import views as sitter_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', sitter_views.sitter_dashboard, name='sitter-dashboard'),
    path('profile', sitter_views.sitter_profile, name = 'sitter-profile'),
    path('edit-profile', sitter_views.edit_sitter_profile, name = 'sitter-edit-profile'),
    path('add-listing', sitter_views.add_listing, name = 'sitter-add-listing'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
