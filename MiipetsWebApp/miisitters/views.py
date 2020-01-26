from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from core.decorators import miisitter_required
from core.models import User, Pets
from .forms import UpdateMiiSitterProfile, AddListing
import datetime

@login_required(login_url='core-login')
@miisitter_required
def sitter_dashboard(request):
    """
    This view allows sitter to view dashboard
    """

    context = {
        "title":"Dashboard",
        "sitter_user":True,
        "total_listings":0,
        "total_reviews":0,
        "total_bookings":0
    }
    return render(request, 'miisitters/sitter-db.html', context)


@login_required(login_url='core-login')
@miisitter_required
def sitter_profile(request):
    """
    This view allows sitter to view dashboard
    """

    context = {
        "title": "Sitter Profile",
        "sitter_user":True,
    }
    return render(request, 'miisitters/sitter-profile.html', context)


@login_required(login_url='core-login')
@miisitter_required
def edit_sitter_profile(request):
    """
    This view edits the profile of the sitter.
    """

    if request.method == 'POST':
        form = UpdateMiiSitterProfile(request.POST, request.FILES, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('sitter-profile')
    else:
        form = UpdateMiiSitterProfile(instance = request.user)

    context = {'form':form, "sitter_user":True,}

    return render(request, 'miisitters/edit-sitter-profile.html', context)


@login_required(login_url='core-login')
@miisitter_required
def add_listing(request):
    """
    This view allows a sitter to add a listing
    """

    if request.method == 'POST':
        form = AddListing(request.POST, request.FILES, user = request.user)

        if form.is_valid():
            form.save(request)
            return redirect('sitter-profile')
    else:
        form = AddListing(user = request.user)

    context = {
        'form':form,
        'title':"Add Listing",
        "sitter_user":True
        }

    return render(request, 'miisitters/sitter-add-listing.html', context)
