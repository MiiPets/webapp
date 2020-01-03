from django.urls import path
from . import views as core_views

urlpatterns = [
    path('', core_views.home, name='core-home'),
    path('about/', core_views.about, name='core-about'),
    path('contact/', core_views.contact, name='core-contact'),
    path('faq/', core_views.faq, name='core-faq'),
    path('logout/', core_views.logout_view, name='core-logout'),
    path('register/', core_views.register, name='core-register'),
    path('register/owner/', core_views.MiiOwnerSignUpView.as_view(), name='core-owner-register'),
    path('register/sitter/', core_views.MiiSitterSignUpView.as_view(), name='core-sitter-register'),
]
