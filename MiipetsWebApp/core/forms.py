from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import MiiOwner, MiiSitter, User
from crispy_forms.helper import FormHelper

class MiiOwnerSignUpForm(UserCreationForm):
    """
    This sign up form allows MiiOwners to register on the site
    and will ascociate the user as a MiiOwner.
    """

    def __init__(self, *args, **kwargs):
        super(MiiOwnerSignUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None


    email = forms.EmailField(required = True)
    name = forms.CharField(required = True)
    surname = forms.CharField(required = True)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_owner = True
        user.first_name = self.cleaned_data.get('name')
        user.last_name = self.cleaned_data.get('surname')
        user.email = self.cleaned_data.get('email')
        user.save()
        miiowner = MiiOwner.objects.create(user=user)
        return user


class MiiSitterSignUpForm(UserCreationForm):
    """
    This sign up form allows MiiOwners to register on the site
    and will ascociate the user as a MiiOwner.
    """

    def __init__(self, *args, **kwargs):
        super(MiiSitterSignUpForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()

        for fieldname in ['username', 'password1', 'password2']:
                self.fields[fieldname].help_text = None


    email = forms.EmailField(required = True)
    name = forms.CharField(required = True)
    surname = forms.CharField(required = True)
    phonenumber = forms.CharField(required = True, label = "For example 27000000000")

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_sitter = True
        user.first_name = self.cleaned_data.get('name')
        user.last_name = self.cleaned_data.get('surname')
        user.email = self.cleaned_data.get('email')
        user.save()
        miisitter = MiiSitter.objects.create(user=user)
        miisitter.contact_number = self.cleaned_data.get('phonenumber')
        miisitter.save()
        return user
