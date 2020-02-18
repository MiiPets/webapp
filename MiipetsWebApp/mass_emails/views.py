from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.views.generic import CreateView
from core.models import User
from core.decorators import superuser_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail
from django.conf import settings

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
            print("Sending to {} at email {}".format(first_name, email))
            subject = 'MiiPets is days from launching!'
            html_message = render_to_string(template,
                                            {'first_name': first_name})
            plain_message = strip_tags(html_message)
            from_email = 'info@miipets.com'
            to = email
            try:
                mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
            except mail.BadHeaderError:
                return HttpResponse('Invalid header found.')

    context= {
        "who":"All Pet sitters",
        "what":"Notifying them that services can be added",
        "template":template
    }

    return render(request, "mass_emails/press_before_send.html", context)
