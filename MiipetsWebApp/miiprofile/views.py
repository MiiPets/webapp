from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from core.decorators import miiowner_required
from core.models import User, Pets
from .forms import UpdateMiiOwnerProfile

@login_required(login_url='core-login')
@miiowner_required
def owner_profile(request):
    """
    This view display the profile of the user.
    """

    pets = Pets.objects.filter(owner = request.user)


    context = {
        "title": "{} profile".format(request.user.first_name),
        "pets":pets
        }

    return render(request, 'miiprofile/user-profile.html', context)


@login_required(login_url='core-login')
@miiowner_required
def edit_owner_profile(request):
    """
    This view display the profile of the user.
    """

    if request.method == 'POST':
        form = UpdateMiiOwnerProfile(request.POST, request.FILES, instance = request.user)
        #form.actual_user = request.user
        if form.is_valid():
            form.save()
            return redirect('profile-profile-owner')
    else:
        form = UpdateMiiOwnerProfile(instance = request.user)

    context = {'form':form}

    return render(request, 'miiprofile/edit-profile.html', context)
