from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View

from .models import Metrics

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
