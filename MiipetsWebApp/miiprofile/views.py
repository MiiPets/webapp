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
    This view edits the profile of the user.
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


@login_required(login_url='core-login')
def view_owner_profile(request, owner_id):
    """
    This view edits the profile of the user.
    """

    owner = User.objects.get(id=owner_id)
    pets = Pets.objects.filter(owner=owner)

    context = {
        "owner":owner,
        "sitter_user":True,
        "pets":pets
    }

    return render(request, 'miiprofile/sitter-profile-view-owner.html', context)
