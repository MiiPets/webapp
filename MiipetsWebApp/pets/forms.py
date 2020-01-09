from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from core.models import User, Pets
from crispy_forms.helper import FormHelper
from django.core.files.uploadedfile import SimpleUploadedFile


class AddPetProfile(forms.ModelForm):

    DOG = 'DOG'
    CAT = 'CAT'
    BIRD = 'DAYCARE'
    REPTILE = 'FEED'
    OTHER = 'OTHER'

    BREED_CHOICES = [(DOG, 'Dog'),
                     (CAT, 'Cat'),
                     (BIRD, 'Bird'),
                     (REPTILE, 'Reptile'),
                     (OTHER, 'Other')]

    type = forms.ChoiceField(choices = BREED_CHOICES, required=True)
    name = forms.CharField(required=True)
    age = forms.IntegerField()
    breed = forms.CharField(max_length=50, required=True)
    profile_picture = forms.ImageField()

    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user',None)
         super(AddPetProfile, self).__init__(*args, **kwargs)


    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['profile_picture','name', 'type', 'breed', 'age']


    @transaction.atomic
    def save(self):
        
        pet = Pets.objects.create(owner=self.user,
                                  name = self.cleaned_data.get('name'),
                                  type = self.cleaned_data.get('type'),
                                  age = self.cleaned_data.get('age'),
                                  breed = self.cleaned_data.get('breed'),
                                  profile_picture = self.cleaned_data.get('profile_picture'))
        return pet
