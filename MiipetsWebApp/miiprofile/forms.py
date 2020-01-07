from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from core.models import MiiOwner, MiiSitter, User
from crispy_forms.helper import FormHelper
from django.core.files.uploadedfile import SimpleUploadedFile


class UpdateMiiOwnerProfile(forms.ModelForm):

    profile_picture = forms.ImageField()
    #username = forms.CharField()
    #email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['profile_picture', 'first_name', 'last_name']

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.profile_picture = self.cleaned_data.get('profile_picture')
        user.save()
        return user
