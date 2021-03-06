from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import View
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.views.generic import CreateView
from .forms import MiiOwnerSignUpForm, MiiSitterSignUpForm, ContactForm, AgreeToTerms
from .models import User, Metrics
from .decorators import miiowner_required, miisitter_required
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core import mail
from django.conf import settings


def send_email_sign_up(first_name, email_address, is_sitter=False):
    """
    Send email to user after sign up
    """

    subject = 'Welcome to MiiPets'
    html_message = render_to_string('core/sitter_welcome_email.html',
                                    {'first_name': first_name, 'is_sitter':is_sitter})
    plain_message = strip_tags(html_message)
    from_email = 'info@miipets.com'
    to = email_address
    try:
        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
    except mail.BadHeaderError:
        return HttpResponse('Invalid header found.')


def get_latest_metrics_for_about():
    """
    This function returns the latest metrics required for the
    about page to show case how many users and activity is on
    the site. The function takes no arguments and returns the
    data in the following form (take note it is not a list):

    total_owners, total_sitters, total_providers, total_pets
    """

    latest_metrics = Metrics.objects.first()
    total_owners = latest_metrics.total_owners
    total_pets = latest_metrics.total_pets
    total_sitters = latest_metrics.total_sitters
    total_providers = latest_metrics.total_providers

    return total_owners, total_sitters, total_providers, total_pets


class MiiOwnerSignUpView(CreateView):
    """
    Used to crete a new MiiOwner user and allow this user
    to only access certain parts of the website.
    """

    model = User
    form_class = MiiOwnerSignUpForm
    template_name = 'core/register_final.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'MiiOwner'
        kwargs['title'] = 'Register'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        send_email_sign_up(user.first_name.upper(), user.email, False)
        return redirect('core-home')


class MiiSitterSignUpView(CreateView):
    """
    Used to crete a new MiiSitter user and allow this user
    to only access certain parts of the website.
    """

    model = User
    form_class = MiiSitterSignUpForm
    template_name = 'core/register_final.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'MiiSitter'
        kwargs['title'] = 'Register'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        send_email_sign_up(user.first_name.upper(), user.email, True)
        return redirect('core-home')


def home(request):
    """
    Home page view
    """

    try:
        if request.user.is_sitter:
            context= {
                "title":"Home",
                'sitter_user':True,
                "google_api":str(settings.GOOGLE_API_KEY),
            }
        else:
            context= {
                "title":"Home",
                "google_api":str(settings.GOOGLE_API_KEY),
            }
    except:
        context= {
            "title":"Home",
            "google_api":str(settings.GOOGLE_API_KEY),
        }
    return render(request, 'core/home.html', context)


def about(request):
    """
    About page view
    """

    total_owners, total_sitters, total_providers, total_pets = get_latest_metrics_for_about()

    try:
        if request.user.is_sitter:
            context = {
                "title":"About",
                "total_miiowners":total_owners,
                "total_pets":total_pets,
                "total_miisitters":total_sitters,
                "total_miiproviders":total_providers,
                "sitter_user":True
                }
        else:
            context = {
                "title":"About",
                "total_miiowners":total_owners,
                "total_pets":total_pets,
                "total_miisitters":total_sitters,
                "total_miiproviders":total_providers,
                }
    except:
        context = {
            "title":"About",
            "total_miiowners":total_owners,
            "total_pets":total_pets,
            "total_miisitters":total_sitters,
            "total_miiproviders":total_providers,
            }
    print(context)
    return render(request, 'core/about.html', context)


def contact(request):
    """
    Contact us page view
    """
    send = False

    if request.method == 'GET':
        form = ContactForm()
        send = False
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']
            try:
                mail.send_mail(subject,
                               message + "\n FROM: {}".format(from_email),
                               'info@miipets.com', ['info@miipets.com'])
            except mail.BadHeaderError:
                return HttpResponse('Invalid header found.')
            send = True
            form = ContactForm()


    try:
        if request.user.is_sitter:
            print("HERE")
            context= {
                "title":"Contact Us",
                "sitter_user":True,
                "send":send,
                "form":form,
                "google_api":str(settings.GOOGLE_API_KEY),
            }
        else:
            context={
                "title":"Contact Us",
                "send":send,
                "form":form,
                "google_api":str(settings.GOOGLE_API_KEY),
            }
    except:
        context= {
            "title":"Contact Us",
            "send":send,
            "form":form,
            "google_api":str(settings.GOOGLE_API_KEY),
        }

    return render(request, "core/contact.html", context)



def faq(request):
    """
    FAQ us page view
    """
    try:
        if request.user.is_sitter:
            context= {
                "title":"FAQ",
                'sitter_user':True
            }
        else:
            context= {
                "title":"FAQ"
            }
    except:
        context= {
            "title":"FAQ"
        }

    return render(request, 'core/faq.html', context)


def register(request):
    """
    View that asked the new user if they want to register
    as a sitter or owner.
    """
    try:
        if request.user.is_sitter:
            context = {
                "title":"Register",
                "sitter_user":True
                }
        else:
            context = {
                "title":"Register",
                "sitter_user":False
                }
    except:
        context = {
            "title":"Register",
            "sitter_user":False
            }

    return render(request, 'core/register.html', context)


def logout_view(request):
    logout(request)
    return redirect('core-home')


def terms_and_conditions(request):
    """
    View that displays the terms and conditions
    """
    
    try:
        if request.user.is_sitter:
            context = {
                "title":"Terms and Conditions",
                "sitter_user":True
                }
        else:
            context = {
                "title":"Terms and Conditions",
                "sitter_user":False
                }
    except:
        context = {
            "title":"Terms and Conditions",
            "sitter_user":False
            }

    return render(request, 'core/tcs.html', context)


def privacy(request):
    """
    View that displays the Privacy policy
    """
    try:
        if request.user.is_sitter:
            context = {
                "title":"Privacy Policy",
                "sitter_user":True
                }
        else:
            context = {
                "title":"Privacy Policy",
                "sitter_user":False
                }
    except:
        context = {
            "title":"Privacy Policy",
            "sitter_user":False
            }

    return render(request, 'core/privacy.html', context)


def agree_to_terms(request):
    """
    View that displays the terms and conditions
    """

    if request.method == 'POST':
        form = AgreeToTerms(request.POST, user=request.user)
        #form.actual_user = request.user
        if form.is_valid():
            form.save()
            return redirect('core-home')
    else:
        form = AgreeToTerms(user=request.user)

    try:
        if request.user.is_sitter:
            context = {
                "title":"Agreement to terms",
                "form":form,
                "sitter_user":True
                }
        else:
            context = {
                "title":"Agreement to terms",
                "form":form,
                "sitter_user":False
                }
    except:
        context = {
            "title":"Agreement to terms",
            "form":form,
            "sitter_user":False
            }
    return render(request, 'core/require_agreement.html', context)


def error_404(request, exception):
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

    return render(request, 'core/404.html', context)