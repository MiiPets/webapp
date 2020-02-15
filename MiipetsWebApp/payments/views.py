from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from core.decorators import  agreed_terms_required
from core.models import SitterServices, MiiSitter
from core.models import ServiceBooking, ServiceLocation, ServiceReviews
from core.methods import create_signature
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def checkout_payment(request, booking_id):

    booking = ServiceBooking.objects.get(id=booking_id)
    sitter = MiiSitter.objects.get(user = booking.service.sitter)

    payfast_url = "https://sandbox.payfast.co.za/eng/process"
    merchant_id = 10000100
    merchant_key = "46f0cd694581a"
    return_url = "http://105.226.65.156:8000/payments/payment-complete.com"
    cancel_url = "http://105.226.65.156:8000/payments/cancel-payment.com"
    notify_url = "http://105.226.65.156:8000/payments/notify-payment.com"
    name_first = booking.requester.first_name
    name_last = booking.requester.last_name
    email_address = booking.requester.email
    m_payment_id = sitter.merchant_id+"_"+str(booking.id)
    amount = "{:.2f}".format(round(float(booking.price),2))
    item_name = booking.service.service_name
    item_description = booking.service.service_name
    email_confirmation = 1
    confirmation_address = 'info@miipets.com'

    list_of_values = {
        "merchant_id":merchant_id,
        "merchant_key":merchant_key,
        "return_url":return_url,
        "cancel_url":cancel_url,
        "notify_url":notify_url,
        "name_first":name_first,
        "name_last":name_last,
        "email_address":email_address,
        "m_payment_id":m_payment_id,
        "amount":amount,
        "item_name":item_name,
        "item_description":item_description,
        "email_confirmation":email_confirmation,
        "confirmation_address":confirmation_address,
    }

    signature = create_signature(list_of_values)

    context = {
        "payfast_url":payfast_url,
        "merchant_id":merchant_id,
        "merchant_key":merchant_key,
        "return_url":return_url,
        "cancel_url":cancel_url,
        "notify_url":notify_url,
        "name_first":name_first,
        "name_last":name_last,
        "email_address":email_address,
        "m_payment_id":m_payment_id,
        "amount":amount,
        "item_name":item_name,
        "item_description":item_description,
        "email_confirmation":email_confirmation,
        "confirmation_address":confirmation_address,
        "signature":signature,
        "sitter_merchant_id":"14938518",
        "booking":booking
    }

    return render(request, 'payments/checkout.html', context)


@login_required(login_url='core-login')
@agreed_terms_required
def success_payment(request, booking_id):
    booking = ServiceBooking.objects.get(id=booking_id)

    return render(request, 'payments/sucess.html', {"booking":booking})


@login_required(login_url='core-login')
@agreed_terms_required
def paysoft_check(request):

    return render(request, 'payments/sucess.html', context)
