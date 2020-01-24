from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from core.models import  MiiSitter, User, SitterServices
from crispy_forms.helper import FormHelper
from django.core.files.uploadedfile import SimpleUploadedFile
from djmoney.forms.fields import MoneyField
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput

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


class AddListing(forms.ModelForm):

    widget_time = forms.widgets.DateTimeInput(attrs={'type':'time'})
    widget_date = forms.widgets.DateTimeInput(attrs={'type':'date'})

    WALK = 'WALK'
    BOARD = 'BOARD'
    SIT = 'SIT'
    DAYCARE = 'DAYCARE'

    SERVICE_CHOICES = [(WALK, 'Walking'),
                       (BOARD, 'House Boarding'),
                       (SIT, 'House Sitting/Feeding'),
                       (DAYCARE, 'Daycare')]

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

    SERVICE_CHOICES = [(WALK, 'Walking'),
                       (BOARD, 'House Boarding'),
                       (SIT, 'House Sitting/Feeding'),
                       (DAYCARE, 'Daycare')]

    TIME_CHOICES = [(NOT_AVAILIBE, 'Not availibe'),
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

    service_name = forms.CharField()
    type = forms.ChoiceField(choices = SERVICE_CHOICES, required=True)
    description = forms.CharField(widget=forms.Textarea)

    price = MoneyField(default_currency='ZAR')
    main_picture = forms.ImageField()
    extra_pictures = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    Service_start_date = forms.BooleanField(widget=DateInput())
    Service_end_date = forms.BooleanField(widget=DateInput())

    Monday_start_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)
    Monday_end_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)

    Tuesday_start_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)
    Tuesday_end_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)

    Wednesday_start_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)
    Wednesday_end_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)

    Thursday_start_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)
    Thursday_end_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)

    Friday_start_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)
    Friday_end_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)

    Saturday_start_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)
    Saturday_end_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)

    Sunday_start_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)
    Sunday_end_time = forms.ChoiceField(choices = TIME_CHOICES, required=True)

    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user',None)
         super(AddListing, self).__init__(*args, **kwargs)


    class Meta(UserCreationForm.Meta):
        model = SitterServices
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
