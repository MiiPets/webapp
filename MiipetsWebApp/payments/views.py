from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from core.decorators import  agreed_terms_required
from core.models import SitterServices, MiiSitter, PayFastOrder
from core.models import ServiceBooking, ServiceLocation, ServiceReviews
from core.methods import create_signature
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail
from django.conf import settings


def send_sitter_payment_confirmation(first_name, email_address, booking):
    """
    Send email to user after sign up
    """

    subject = 'MiiPets Payment Confirmation'
    html_message = render_to_string('payments/owner_payment_confirmation_email.html',
                                    {'first_name': first_name,'booking':booking})
    plain_message = strip_tags(html_message)
    from_email = 'info@miipets.com'
    to = email_address
    try:
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    except mail.BadHeaderError:
        return HttpResponse('Invalid header found.')


def send_sitter_payment_confirmation(first_name, email_address, booking):
    """
    Send email to user after sign up
    """

    subject = 'Your MiiOwner has payed'
    html_message = render_to_string('payments/sitter_payment_confirmation_email.html',
                                    {'first_name': first_name,'booking':booking})
    plain_message = strip_tags(html_message)
    from_email = 'info@miipets.com'
    to = email_address
    try:
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    except mail.BadHeaderError:
        return HttpResponse('Invalid header found.')


@csrf_exempt
def checkout_payment(request, booking_id):

    booking = ServiceBooking.objects.get(id=booking_id)
    sitter = MiiSitter.objects.get(user = booking.service.sitter)

    payfast_url = "https://sandbox.payfast.co.za/eng/process"
    merchant_id = 10016213
    merchant_key = "qpy7a8jq1hgz1"
    return_url = "http://miipets.com:8080/payments/payment-complete/{}".format(booking.id)
    cancel_url = "http://miipets.com:8080/payments/cancel-payment"
    notify_url = "http://miipets.com:8080/payments/notify-payment"
    name_first = (booking.requester.first_name).replace(" ", "")
    name_last = (booking.requester.last_name).replace(" ", "")
    email_address = (booking.requester.email).replace(" ", "")
    m_payment_id = (sitter.merchant_id+"_"+str(booking.id)).replace(" ", "")
    amount = "{:.2f}".format(round(float(booking.price),2))
    item_name = (booking.service.service_name).replace(" ", "")
    item_description = (booking.service.service_name).replace(" ", "")
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
        "sitter_merchant_id":"10016213",
        "booking":booking
    }

    # saving order
    try:
        already_there = PayFastOrder.objects.filter(m_payment_id = m_payment_id)
        if len(already_there) >= 1:
            pass
        else:
            PayFastOrder.objects.create(payfast_url = payfast_url,
                                        merchant_id = merchant_id,
                                        merchant_key = merchant_key,
                                        return_url = return_url,
                                        cancel_url = cancel_url,
                                        notify_url = notify_url,
                                        name_first = name_first,
                                        name_last = name_last,
                                        email_address = email_address,
                                        m_payment_id = m_payment_id,
                                        amount = amount,
                                        item_name = item_name,
                                        item_description = item_description,
                                        email_confirmation = str(email_confirmation),
                                        confirmation_address = confirmation_address,
                                        signature = signature,
                                        sitter_merchant_id = sitter.merchant_id,
                                        booking = booking)
    except:
        PayFastOrder.objects.create(payfast_url = payfast_url,
                                    merchant_id = merchant_id,
                                    merchant_key = merchant_key,
                                    return_url = return_url,
                                    cancel_url = cancel_url,
                                    notify_url = notify_url,
                                    name_first = name_first,
                                    name_last = name_last,
                                    email_address = email_address,
                                    m_payment_id = m_payment_id,
                                    amount = amount,
                                    item_name = item_name,
                                    item_description = item_description,
                                    email_confirmation = str(email_confirmation),
                                    confirmation_address = confirmation_address,
                                    signature = signature,
                                    sitter_merchant_id = sitter.merchant_id,
                                    booking = booking)


    return render(request, 'payments/checkout.html', context)


@login_required(login_url='core-login')
@agreed_terms_required
def success_payment(request, booking_id):
    booking = ServiceBooking.objects.get(id=booking_id)
    return render(request, 'payments/sucess.html', {"booking":booking})


@login_required(login_url='core-login')
@agreed_terms_required
def cancel_payment(request):
    return render(request, 'payments/cancel.html')


@csrf_exempt
def paysoft_check(request):
    """
    Notify URL handler.
    On successful access 'payfast.signals.notify' signal is sent.
    Orders should be processed in signal handler.
    """

    m_payment_id = request.POST.get('m_payment_id', None)
    order = get_object_or_404(PayFastOrder, m_payment_id=m_payment_id)

    print("HELLLOOO!!!")
    print(request.POST)

    # is signature valid
    list_of_values = {
          "m_payment_id":request.POST.get('m_payment_id', None),
          "pf_payment_id":request.POST.get('pf_payment_id', None),
          "payment_status":request.POST.get('payment_status', None),
          "item_name":request.POST.get('item_name', None),
          "item_description":request.POST.get('item_description', None),
          "amount_gross":request.POST.get('amount_gross', None),
          "amount_fee":request.POST.get('amount_fee', None),
          "amount_net":request.POST.get('amount_net', None),
          'custom_str1':request.POST.get("custom_str1", None),
          'custom_str2':request.POST.get("custom_str2", None),
          'custom_str3':request.POST.get("custom_str3", None),
          'custom_str4':request.POST.get("custom_str4", None),
          'custom_str5':request.POST.get("custom_str5", None),
          'custom_int1':request.POST.get("custom_int1", None),
          'custom_int2':request.POST.get("custom_int2", None),
          'custom_int3':request.POST.get("custom_int3", None),
          'custom_int4':request.POST.get("custom_int4", None),
          'custom_int5':request.POST.get("custom_int5", None),
          "name_first":request.POST.get('name_first', None),
          "name_last":request.POST.get('name_last', None),
          "email_address":request.POST.get('email_address', None),
          "merchant_id":request.POST.get('merchant_id', None)
        }

    print("VALUES:")
    print(list_of_values)
    signature = create_signature(list_of_values)

    print("THERE SIGNATURE: {}".format(request.POST.get('signature', None)))

    if signature == request.POST.get('signature', None):
        pass
    else:
        print("PAYMENT FAILED BECAUSE: signatures did not match")
        return HttpResponseBadRequest()

    # is request IP in trusted sources
    domain = request.META['HTTP_REFERER']
    valid_domains = ["www.payfast.co.za", "w1w.payfast.co.za", "w2w.payfast.co.za", "sandbox.payfast.co.za"]
    if domain.split("https://")[1] in valid_domains:
       pass
    else:
       print("PAYMENT FAILED BECAUSE: IP is not trusted")
       return HttpResponseBadRequest()

    try:
        if str(order.amount).split(".")[0] == str(request.POST.get('amount_gross', None)).split(".")[0]:
            pass
        else:
            print("PAYMENT FAILED BECAUSE: amount is different")
            print("US:{} THEY:{}".format(order.amount, request.POST.get('amount_gross', None)))
            return HttpResponseBadRequest()
    except:
        print("IN THE EXCEPT")
        if order.amount == request.POST.get('amount_gross', None):
            pass
        else:
            print("PAYMENT FAILED BECAUSE: amount is different")
            print("US:{} THEY:{}".format(order.amount, request.POST.get('amount_gross', None)))
            return HttpResponseBadRequest()

    if order.item_description == request.POST.get('item_description', None):
        pass
    else:
        print("PAYMENT FAILED BECAUSE: item_description are different")
        print("US:{} THEY:{}".format(order.item_description, request.POST.get('item_description', None)))
        return HttpResponseBadRequest()

    if order.name_first == request.POST.get('name_first', None):
        pass
    else:
        print("PAYMENT FAILED BECAUSE: name_first are different")
        print("US:{} THEY:{}".format(order.name_first, request.POST.get('name_first', None)))
        return HttpResponseBadRequest()

    if order.name_last == request.POST.get('name_last', None):
        pass
    else:
        print("PAYMENT FAILED BECAUSE: name_last are different")
        print("US:{} THEY:{}".format(order.name_last, request.POST.get('name_last', None)))
        return HttpResponseBadRequest()

    if order.email_address == request.POST.get('email_address', None):
        pass
    else:
        print("PAYMENT FAILED BECAUSE: email_address are different")
        print("US:{} THEY:{}".format(order.email_address, request.POST.get('email_address', None)))
        return HttpResponseBadRequest()

    if order.merchant_id == request.POST.get('merchant_id', None):
        pass
    else:
        print("PAYMENT FAILED BECAUSE: merchant_id are different")
        print("US:{} THEY:{}".format(order.merchant_id, request.POST.get('merchant_id', None)))
        return HttpResponseBadRequest()


    # data has not been processed yet
    print("NOW I AM HERE")
    post_bytes = urllib.parse.urlencode(list_of_values, encoding='utf-8', errors='strict').encode('ascii')
    response = urllib.request.urlopen("https://sandbox.payfast.co.za/eng/query/validate", data=post_bytes)
    result = response.read().decode('utf-8')
    print("RESULT:{}".format(result))

    if result:
        pass
    else:
        print("PAYMENT FAILED BECAUSE: data has not been sent by payfast")
        return HttpResponseBadRequest()

    # pf_payment_id not somewhere in database perhaps
    try:
        orders = PayFastOrder.objects.filter(pf_payment_id = request.POST.get('pf_payment_id', None))
    except:
        orders = []

    if len(orders) >= 1:
        print("PAYMENT FAILED BECAUSE: Payment has already been processed")
        return HttpResponseBadRequest()
    else:
        pass

    # update model to reflect payment
    order.pf_payment_id =  request.POST.get('pf_payment_id', None)
    order.payment_status = request.POST.get('payment_status', None)
    order.amount_gross = request.POST.get('amount_gross', None)
    order.amount_fee = request.POST.get('amount_fee', None)
    order.amount_net = request.POST.get('amount_net', None)
    order.signature_from_payfast = request.POST.get('signature', None)
    order.trusted = True
    order.went_to_payfast = True
    order = form.save(update_fields = ["pf_payment_id", "payment_status", "amount_gross", "went_to_payfast",
                                       "amount_fee", "amount_net", "signature_from_payfast","trusted"])


    if not order.notified_sitter:
        try:
            send_sitter_payment_confirmation(order.booking.service.sitter.first_name,
                                             order.booking.service.sitter.email,
                                             order.booking)
            order.notified_sitter = True
            order = form.save(update_fields = ['notified_sitter'])
        except:
            print('could not notify sitter in payment')

    if not oder.notified_owner:
        try:
            send_owner_payment_confirmation(order.booking.requester.first_name,
                                            order.booking.requester.email,
                                            order.booking)
            order.notified_owner = True
            order = form.save(update_fields = ['notified_sitter'])
        except:
            print('could not notify sitter in payment')

    # notify owner and sitter that payment has been made and booking confirmed
    print("MADE IT TO THE END!!")

    return HttpResponse()
