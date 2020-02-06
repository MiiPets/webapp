from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from core.models import  MiiSitter, User, SitterServices, ServiceBooking
from crispy_forms.helper import FormHelper
from django.core.files.uploadedfile import SimpleUploadedFile
from djmoney.forms.fields import MoneyField
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from core.methods import calculate_number_of_days, return_day_of_week_from_date

class DateInput(forms.DateInput):
    input_type = 'date'


class BookService(forms.ModelForm):

    class Meta():
        model = ServiceBooking
        fields = []

    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user',None)
         self.service = kwargs.pop('service', None)

         TIME_CHOICES = [(9999, "Please choose a date first")]

         super(BookService, self).__init__(*args, **kwargs)
         self.fields['start_date'] = forms.DateField(widget=DateInput(), required=True)
         if self.service.type != 'WALK':
            self.fields['end_date'] = forms.DateField(widget=DateInput(), required=True)
         else:
            self.fields['time_slot'] = forms.ChoiceField(choices =TIME_CHOICES, required=True)

    @transaction.atomic
    def save(self):
        booking = super().save(commit=False)

        booking.requester = self.user
        booking.service = self.service
        booking.start_date = self.cleaned_data.get('start_date')
        if self.service.type != "WALK":
            booking.end_date = self.cleaned_data.get('end_date')
        else:
            booking.end_date = '1900-01-01'

        if self.service.type == "WALK":
            booking.time_slot =  self.cleaned_data.get('time_slot')
        else:
            booking.time_slot =  9999

        booking.approved = False
        booking.notified_sitter = False
        booking.sitter_answer = False
        booking.notified_owner_of_sitter_response = False
        booking.sitter_confirmed = False
        booking.invoice_sent = False
        if self.service.type == "Walk":
            number_of_days = 1
        else:
            number_of_days = calculate_number_of_days(self.cleaned_data.get('start_date'),
                                                      self.cleaned_data.get('end_date') )
        booking.price = self.service.price * number_of_days
        booking.price_in_cents = self.service.price * number_of_days * 100
        booking.save()

        return booking
