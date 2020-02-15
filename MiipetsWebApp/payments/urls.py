from django.urls import path
from . import views as payment_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('checkout/<int:booking_id>', payment_views.checkout_payment, name='payments-checkout'),
    path('payment-complete/<int:booking_id>', payment_views.success_payment, name='payments-sucess'),
    path('notify-payment', payment_views.paysoft_check, name='payments-check-payfast'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
