from django.contrib import admin
from django.urls import path
from django.urls import include, path
#from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    #path('register/', owner_views.register, name = 'register'),
]
