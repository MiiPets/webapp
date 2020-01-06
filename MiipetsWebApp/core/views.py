from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.views.generic import CreateView
from .forms import MiiOwnerSignUpForm, MiiSitterSignUpForm
from .models import User, Metrics
from .decorators import miiowner_required, miisitter_required


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
        return redirect('core-home')


def home(request):
    """
    Home page view
    """

    return render(request, 'core/home.html')


def about(request):
    """
    About page view
    """

    total_owners, total_sitters, total_providers, total_pets = get_latest_metrics_for_about()

    context = {
        "title":"About",
        "total_miiowners":total_owners,
        "total_pets":total_pets,
        "total_miisitters":total_sitters,
        "total_miiproviders":total_providers,
        }

    return render(request, 'core/about.html', context)


def contact(request):
    """
    Contact us page view
    """

    context = {
        "title":"Contact Us"
        }

    return render(request, 'core/contact.html', context)


def faq(request):
    """
    FAQ us page view
    """

    context = {
          "title":"FAQ"
          }

    return render(request, 'core/faq.html', context)


def register(request):
    """
    View that asked the new user if they want to register
    as a sitter or owner.
    """

    context = {
          "title":"register"
          }

    return render(request, 'core/register.html', context)


def logout_view(request):
    context = {
        "title":"Login"
    }

    return render(request, 'core/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('core-home')
