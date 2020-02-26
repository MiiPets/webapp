from django.contrib import admin
from django.urls import path
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

def page_not_found(request, exception):
    print("HERE!")
    print(exception)
    try:
        if request.user.is_sitter:
            context = {
                "title":"Page not found",
                "sitter_user":True
                }
        else:
            context = {
                "title":"Page not found",
                "sitter_user":False
                }
    except:
        context = {
            "title":"Page not found",
            "sitter_user":False
            }
    return render(request, 'core/error404.html', context)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('profile/', include('miiprofile.urls')),
    path('pets/', include('pets.urls')),
    path('miidashboard/', include('miisitters.urls')),
    path('services/', include('services.urls')),
    path('payments/', include('payments.urls')),
    path('reviews/', include('reviews.urls')),
    path('mass-emails/', include('mass_emails.urls')),
]

handler404 = 'core.views.error_404'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
