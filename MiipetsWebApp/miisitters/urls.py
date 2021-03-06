from django.urls import path
from . import views as sitter_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', sitter_views.sitter_dashboard, name='sitter-dashboard'),
    path('profile', sitter_views.sitter_profile, name = 'sitter-profile'),
    path('edit-profile', sitter_views.edit_sitter_profile, name = 'sitter-edit-profile'),
    path('add-listing', sitter_views.add_service, name = 'sitter-add-service'),
    path('vetting-in-process', sitter_views.vetting_sitter, name = 'sitter-still-vetting'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
