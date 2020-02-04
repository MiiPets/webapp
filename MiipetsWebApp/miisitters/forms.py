from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from core.models import  MiiSitter, User, SitterServices, ServicePhotos, ServiceLocation
from crispy_forms.helper import FormHelper
from django.core.files.uploadedfile import SimpleUploadedFile
from djmoney.forms.fields import MoneyField
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from googlemaps import Client as GoogleMaps
from core.methods import address_to_lat_long


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'timeselect'


class UpdateMiiSitterProfile(forms.ModelForm):

    profile_picture = forms.ImageField()
    #email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    #contact_number = forms.CharField()
    bio = forms.CharField(widget=forms.Textarea)


    class Meta(UserCreationForm.Meta):
        model = User
        fields = [
            'profile_picture',
            'first_name',
            'last_name',
            #'email',
            #'contact_number',
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


class AddService(forms.ModelForm):

    widget_time = forms.widgets.DateTimeInput(attrs={'type':'time'})
    widget_date = forms.widgets.DateTimeInput(attrs={'type':'date'})

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

    NOT_AVAILIBE = 9999
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    ELEVEN = 11
    TWELVE = 12
    THIRTEEN = 13
    FOURTEEN = 14
    FIFTEEN = 15
    SIXTEEN = 16
    SEVENTEEN = 17
    EIGHTEEN = 18
    NINETEEN = 19
    TWENTY = 20
    TWENTYONE = 21
    TWENTYTWO = 21
    TWENTYTHREE = 23
    TWENTYFOUR = 0

    TIME_CHOICES = [(NOT_AVAILIBE, 'Not availibe on this day'),
                    (ONE, '1:00'),
                    (TWO, '2:00'),
                    (THREE, '3:00'),
                    (FOUR, '4:00'),
                    (FIVE, '5:00'),
                    (SIX, '6:00'),
                    (SEVEN, '7:00'),
                    (EIGHT, '8:00'),
                    (NINE, '9:00'),
                    (TEN, '10:00'),
                    (ELEVEN, '11:00'),
                    (TWELVE, '12:00'),
                    (THIRTEEN, '13:00'),
                    (FOURTEEN, '14:00'),
                    (FIFTEEN, '15:00'),
                    (SIXTEEN, '16:00'),
                    (SEVENTEEN, '17:00'),
                    (EIGHTEEN, '18:00'),
                    (NINETEEN, '19:00'),
                    (TWENTY, '20:00'),
                    (TWENTYONE, '21:00'),
                    (TWENTYTWO, '21:00'),
                    (TWENTYTHREE, '23:00'),
                    (TWENTYFOUR, '00:00'),]

    city = forms.CharField(help_text = "Where you will be providing this service?")
    province = forms.CharField()
    area_code = forms.CharField()
    street_name = forms.CharField(required=False,
                                  help_text="Only required for boarding or daycare services")
    street_number = forms.CharField(required=False,
                                    help_text="Only required for boarding or daycare services")

    main_picture = forms.ImageField(required=True)
    extra_pictures = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),
                                     required=False)

    service_start_date = forms.DateField(widget=DateInput(), required=True)
    service_end_date = forms.DateField(widget=DateInput(), required=True)

    monday_start_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)
    monday_end_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)

    tuesday_start_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)
    tuesday_end_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)

    wednesday_start_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)
    wednesday_end_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)

    thursday_start_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)
    thursday_end_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)

    friday_start_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)
    friday_end_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)

    saturday_start_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)
    saturday_end_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)

    sunday_start_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)
    sunday_end_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)

    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user',None)
         super(AddService, self).__init__(*args, **kwargs)


    class Meta(UserCreationForm.Meta):
        model = SitterServices
        model2 = User
        fields = ["service_name",
                  "type",
                  "description",
                  "price",
                  "dogs_allowed",
                  "cats_allowed",
                  "birds_allowed",
                  "reptiles_allowed",
                  "other_pets_allowed"]


    @transaction.atomic
    def save(self, request):
        service = super().save(commit=False)

        service.sitter = self.user
        service.profile_picture = self.cleaned_data.get('main_picture')
        service.service_name = self.cleaned_data.get('service_name')
        service.type = self.cleaned_data.get('type')
        service.description = self.cleaned_data.get('description')
        service.price = self.cleaned_data.get('price')
        service.date_start= self.cleaned_data.get('service_start_date')
        service.date_end= self.cleaned_data.get('service_end_date')
        service.time_start_monday= self.cleaned_data.get('monday_start_time')
        service.time_start_tuesday= self.cleaned_data.get('tuesday_start_time')
        service.time_start_wednesday= self.cleaned_data.get('wednesday_start_time')
        service.time_start_thursday= self.cleaned_data.get('thursday_start_time')
        service.time_start_friday= self.cleaned_data.get('friday_start_time')
        service.time_start_saturday= self.cleaned_data.get('saturday_start_time')
        service.time_start_sunday= self.cleaned_data.get('sunday_start_time')
        service.time_end_monday= self.cleaned_data.get('monday_end_time')
        service.time_end_tuesday= self.cleaned_data.get('tuesday_end_time')
        service.time_end_wednesday= self.cleaned_data.get('wednesday_end_time')
        service.time_end_thursday= self.cleaned_data.get('thursday_end_time')
        service.time_end_friday= self.cleaned_data.get('friday_end_time')
        service.time_end_saturday= self.cleaned_data.get('saturday_end_time')
        service.time_end_sunday= self.cleaned_data.get('sunday_end_time')
        service.save()

        # create the records for extra pictures
        for file in request.FILES.getlist('extra_pictures'):
            background_photos = ServicePhotos.objects.create(service = service,
                                                             profile_picture = file)

        # create the records for location
        lat, lng = address_to_lat_long(self.cleaned_data.get('city'),
                                        self.cleaned_data.get('province'),
                                        self.cleaned_data.get('street_name'),
                                        self.cleaned_data.get('street_number'),
                                        self.cleaned_data.get('area_code'))


        location = ServiceLocation.objects.create(service = service,
                                                  city = self.cleaned_data.get('city'),
                                                  province = self.cleaned_data.get('province'),
                                                  street_name = self.cleaned_data.get('street_name'),
                                                  area_code = self.cleaned_data.get('area_code'),
                                                  street_number = self.cleaned_data.get('street_number'),
                                                  lattitude = lat,
                                                  longitude = lng)

        return service
