from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from core.decorators import miiowner_required
from core.models import User, Pets, SitterServices


def view_all_listings(request):
    """
    This view allows everyone to view all current listings
    """

    listings = SitterServices.objects.all()

    if request.user.is_sitter:
        context = {
            "title": "All Listings",
            "listings":listings,
            "sitter_user":True
            }
    else:
        context = {
            "title": "All Listings",
            "listings":listings,
            "sitter_user":False
            }

    return render(request, 'listings/all-listings.html', context)