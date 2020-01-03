from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import MiiOwner, MiiSitter, User


class MiiOwnerSignUpForm(UserCreationForm):
    """
    This sign up form allows MiiOwners to register on the site
    and will ascociate the user as a MiiOwner.
    """


    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_owner = True
        user.save()
        miiowner = MiiOwner.objects.create(user=user)
        #miiowner.interests.add(*self.cleaned_data.get('interests'))
        return user


class MiiSitterSignUpForm(UserCreationForm):
    """
    This sign up form allows MiiOwners to register on the site
    and will ascociate the user as a MiiOwner.
    """

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_sitter = True
        user.save()
        miisitter = MiiSitter.objects.create(user=user)
        #miiowner.interests.add(*self.cleaned_data.get('interests'))
        return user
