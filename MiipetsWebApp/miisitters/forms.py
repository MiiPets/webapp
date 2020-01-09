from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from core.models import  MiiSitter, User, SitterServices
from crispy_forms.helper import FormHelper
from django.core.files.uploadedfile import SimpleUploadedFile
from djmoney.forms.fields import MoneyField


class UpdateMiiSitterProfile(forms.ModelForm):

    profile_picture = forms.ImageField()
    #email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    contact_number = forms.CharField()
    bio = forms.CharField(widget=forms.Textarea)


    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'profile_picture',
            'first_name',
            'last_name',
            #'email',
            'contact_number',
            'bio'
        ]

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


class AddListing(forms.ModelForm):

    WALK = 'WALK'
    BOARD = 'BOARD'
    SIT = 'SIT'
    DAYCARE = 'DAYCARE'
    FEED = 'FEED'

    SERVICE_CHOICES = [(WALK, 'Walking'),
                       (BOARD, 'House Boarding'),
                       (SIT, 'House Sitting'),
                       (DAYCARE, 'Daycare'),
                       (FEED, 'Daily feeding and playing')]

    listing_name = forms.CharField()
    type = forms.ChoiceField(choices = SERVICE_CHOICES, required=True)
    description = forms.CharField(widget=forms.Textarea)
    price = MoneyField(default_currency='ZAR')
    listing_picture = forms.ImageField()

    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user',None)
         super(AddListing, self).__init__(*args, **kwargs)


    class Meta(UserCreationForm.Meta):
        model = User
        fields = []


    @transaction.atomic
    def save(self):

        service = SitterServices.objects.create(sitter=self.user,
                                                profile_picture = self.cleaned_data.get('listing_picture'),
                                                listing_name = self.cleaned_data.get('listing_name'),
                                                type = self.cleaned_data.get('type'),
                                                description = self.cleaned_data.get('description'),
                                                price = self.cleaned_data.get('price'))
        return service
