from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.views.generic import CreateView
from core.models import User, ServiceBooking
from core.decorators import superuser_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail
from django.conf import settings
import datetime


@superuser_required(login_url='core-login')
def send_sitter_notification_add_services(request):
    """
    Notify all sitters that the site is live to
    add services.
    """

    sitters = User.objects.filter(is_sitter=True)
    sitter_email_first_names = [[sitter.email, sitter.first_name] for sitter in sitters]
    template = 'mass_emails/anounce_sitter_add_service_ettiquete.html'

    if request.method == 'POST':
        for email, first_name in sitter_email_first_names:
            try:
                print("Sending to {} at email {}".format(first_name, email))
                subject = 'MiiPets is live'
                html_message = render_to_string(template,
                                                {'first_name': first_name})
                plain_message = strip_tags(html_message)
                from_email = 'info@miipets.com'
                to = email
                try:
                    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                except mail.BadHeaderError:
                    return HttpResponse('Invalid header found.')
            except:
                print("Sending to {} at email {} FAILED".format(first_name, email))


    context= {
        "who":"All Pet sitters",
        "what":"Notifying them that services can be added",
        "template":template
    }

    return render(request, "mass_emails/press_before_send.html", context)

@superuser_required(login_url='core-login')
def notify_everyone_bookings_closed(request):
    """
    Notify all owners whose services ended the day before to review their service.
    """
    template = 'mass_emails/miipets_break.html'
    users = User.objects.all()
    if request.method == 'POST':
        for user in users:
            try:
                print("Sending to {} at email {}".format(user.first_name, user.email))
                subject = 'MiiPets and the COVID-19 virus'
                html_message = render_to_string(template,
                                                {'first_name': user.first_name})
                plain_message = strip_tags(html_message)
                from_email = 'ruan@miipets.com'
                to = user.email
                try:
                    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                except mail.BadHeaderError:
                    return HttpResponse('Invalid header found.')
            except:
                print("Sending to {} at email {} FAILED".format(user.first_name, user.email))


    context= {
        "who":"Everyone",
        "what":"Notify of Miipets not taking bookings",
        "template":template
    }

    return render(request, "mass_emails/press_before_send.html", context)


@superuser_required(login_url='core-login')
def send_owners_notification_to_review_service(request):
    """
    Notify all owners whose services ended the day before to review their service.
    """
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    bookings = ServiceBooking.objects.filter(end_date=yesterday)
    template = 'mass_emails/owners_notification_to_review_service.html'
    if request.method == 'POST':
        for booking in bookings:
            try:
                print("Sending to {} at email {}".format(booking.requester.first_name, booking.requester.email))
                subject = 'Please rate your MiiSitter'
                html_message = render_to_string(template,
                                                {'first_name': booking.requester.first_name,
                                                 'booking':booking})
                plain_message = strip_tags(html_message)
                from_email = 'info@miipets.com'
                to = booking.requester.email
                try:
                    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
                except mail.BadHeaderError:
                    return HttpResponse('Invalid header found.')
            except:
                print("Sending to {} at email {} FAILED".format(booking.requester.first_name, booking.requester.email))


    context= {
        "who":"People whos booking ended yesterday",
        "what":"Telling them to review service received",
        "template":template
    }

    return render(request, "mass_emails/press_before_send.html", context)
