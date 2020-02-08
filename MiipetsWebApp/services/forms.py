from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from core.models import  MiiSitter, User, SitterServices, ServiceBooking
from crispy_forms.helper import FormHelper
from django.core.files.uploadedfile import SimpleUploadedFile
from djmoney.forms.fields import MoneyField
from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput
from core.methods import calculate_number_of_days, return_day_of_week_from_date, make_sure_start_before_end_date

class DateInput(forms.DateInput):
    input_type = 'date'


class BookService(forms.ModelForm):

    class Meta():
        model = ServiceBooking
        fields = ['start_date', 'end_date', 'time_slot', 'number_of_pets']

    def __init__(self, *args, **kwargs):
         self.user = kwargs.pop('user',None)
         self.service = kwargs.pop('service', None)
         super(BookService, self).__init__(*args, **kwargs)

         TIME_CHOICES = [(9999, "Please choose a date/number of pets first"),
                         (1,"01:00-02:00"),
                         (2,"02:00-02:00"),
                         (3,"03:00-04:00"),
                         (4,"04:00-05:00"),
                         (5,"05:00-06:00"),
                         (6,"06:00-07:00"),
                         (7,"07:00-08:00"),
                         (8,"08:00-09:00"),
                         (9,"09:00-10:00"),
                         (10,"10:00-11:00"),
                         (11,"11:00-12:00"),
                         (12,"12:00-13:00"),
                         (13,"13:00-14:00"),
                         (14,"14:00-15:00"),
                         (15,"15:00-16:00"),
                         (16,"16:00-17:00"),
                         (17,"17:00-18:00"),
                         (18,"18:00-19:00"),
                         (19,"19:00-20:00"),
                         (20,"20:00-21:00"),
                         (21,"21:00-22:00"),
                         (22,"22:00-23:00"),
                         (23,"23:00-00:00")]

         self.fields['start_date'] = forms.DateField(widget=DateInput(), required=True)
         self.fields["number_of_pets"] = forms.IntegerField(required=True)

         if self.service.type != 'WALK':
            self.fields['end_date'] = forms.DateField(widget=DateInput(),
                                                      required=True)
            self.fields['time_slot'] = forms.ChoiceField(choices =TIME_CHOICES,
                                                         required=False,
                                                         widget = forms.HiddenInput(),)
         else:
            self.fields['end_date'] = forms.CharField(widget = forms.HiddenInput(),
                                                      required = False)
            self.fields['time_slot'] = forms.ChoiceField(choices =TIME_CHOICES, required=True)



    @transaction.atomic
    def save(self):
        booking = super().save(commit=False)

        if self.service.type != "WALK":
            start_date, end_date = make_sure_start_before_end_date(self.cleaned_data.get('start_date'),
                                                                   self.cleaned_data.get('end_date'))
        else:
            start_date = self.cleaned_data.get('start_date')

        booking.requester = self.user
        booking.service = self.service
        booking.start_date = start_date
        if self.service.type != "WALK":
            booking.end_date = end_date
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
        booking.number_of_pets = self.cleaned_data.get('number_of_pets')

        if self.service.type == "WALK":
            number_of_days = 1
        else:
            number_of_days = calculate_number_of_days(self.cleaned_data.get('start_date'),
                                                      self.cleaned_data.get('end_date'))
        booking.price = self.service.price * number_of_days
        booking.price_in_cents = self.service.price * number_of_days * 100
        booking.save()

        return booking
