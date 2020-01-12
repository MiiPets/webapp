from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from core.decorators import miiowner_required
from core.models import User, Pets
from .forms import AddPetProfile


@login_required(login_url='core-login')
@miiowner_required
def add_pet_profile(request):
    data = request.DATA
    """
    This view allows user to add a pet
    """

    if request.method == 'POST':
        form = AddPetProfile(request.POST, request.FILES, user = request.user ) #, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('profile-profile-owner')
    else:
        form = AddPetProfile(user = request.user)#instance = request.user)

    context = {'form':form}

    return render(request, 'pets/add-pet.html', context)
