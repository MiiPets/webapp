from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from core.decorators import miisitter_required, validation_required
from core.decorators import merchant_id_required, sitter_id_required
from core.models import User, Pets, MiiSitter, SitterServices
from .forms import UpdateMiiSitterProfile, AddService
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
    services = SitterServices.objects.filter(sitter=request.user)
    context = {
        "title": "Sitter Profile",
        "sitter_user":True,
        'services':services
    }
    return render(request, 'miisitters/sitter-profile.html', context)


@login_required(login_url='core-login')
@miisitter_required
def edit_sitter_profile(request):
    """
    This view edits the profile of the sitter.
    """

    sitter_details = MiiSitter.objects.get(user = request.user)
    initial = {'merchant_id':sitter_details.merchant_id,
               'id_number':sitter_details.id_number}

    if request.method == 'POST':
        form = UpdateMiiSitterProfile(request.POST, request.FILES, initial=initial,
                                      instance = request.user, user = request.user)
        if form.is_valid():
            form.save()
            return redirect('sitter-profile')
    else:
        form = UpdateMiiSitterProfile(initial=initial, instance = request.user)

    context = {'form':form, "sitter_user":True,}

    return render(request, 'miisitters/edit-sitter-profile.html', context)


@login_required(login_url='core-login')
@miisitter_required
@validation_required
@merchant_id_required
@sitter_id_required
def add_service(request):
    """
    This view allows a sitter to add a listing
    """

    if request.method == 'POST':
        form = AddService(request.POST, request.FILES, user = request.user)

        if form.is_valid():
            form.save(request)
            return redirect('sitter-profile')
    else:
        form = AddService(user = request.user)

    sitter_details = MiiSitter.objects.get(user=request.user)

    context = {
        'form':form,
        'title':"Add Listing",
        "sitter_user":True,
        }

    return render(request, 'miisitters/sitter-add-service.html', context)


def vetting_sitter(request):
    """
    Page that is shown to users when their profile
    has not been vetted yet which means they can not add
    services yet
    """

    return render(request, 'miisitters/validation_required.html', {"sitter_user":True})
