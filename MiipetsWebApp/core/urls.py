from django.urls import path, re_path
from . import views as core_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', core_views.home, name='core-home'),
    path('about/', core_views.about, name='core-about'),
    path('contact/', core_views.contact, name='core-contact'),
    path('faq/', core_views.faq, name='core-faq'),
    path('logout/', core_views.logout_view, name='core-logout'),
    path('login', auth_views.LoginView.as_view() , name='core-login'),
    path('register/', core_views.register, name='core-register'),
    path('register/owner/', core_views.MiiOwnerSignUpView.as_view(), name='core-owner-register'),
    path('register/sitter/', core_views.MiiSitterSignUpView.as_view(), name='core-sitter-register'),
    path('terms-and-conditions/', core_views.terms_and_conditions, name='core-tcs'),
    path('privacy/', core_views.privacy, name='core-privacy'),
    path('agree-to-terms/', core_views.agree_to_terms, name='core-agree-to-terms'),
    path('password_reset', auth_views.PasswordResetView.as_view(html_email_template_name='registration/password_reset_email.html'), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
          auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
