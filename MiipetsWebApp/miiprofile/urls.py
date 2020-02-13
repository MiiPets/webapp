from django.urls import path
from . import views as profile_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', profile_views.owner_profile, name='profile-profile-owner'),
    path('edit-profile/', profile_views.edit_owner_profile, name='profile-edit-owner'),
    path('view-miiowner-profile/<int:owner_id>', profile_views.view_owner_profile, name='sitter-view-owner-profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
