from django.urls import path
from . import views as core_views

urlpatterns = [
    path('', core_views.home, name='core-home'),
    path('about/', core_views.about, name='core-about'),
    path('contact/', core_views.contact, name='core-contact'),
    path('faq/', core_views.faq, name='core-faq'),
]
