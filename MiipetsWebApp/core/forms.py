from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import MiiOwner, MiiSitter, User
from crispy_forms.helper import FormHelper

def check_if_id_is_valid(id_string):
    '''
    This function will check if the ID given is valid or not and will return true
    if it valid and false is it is not.

    Example input:
        9202204720082
        1703295010174

    Example output:
        False
        True
    '''

    check_number = int(id_string[-1])
    sum_ = 0

    # calculating sum
    for n in range(0,12):
        d = int(id_string[-2-n])

        if n%2 == 0:
            sum_ = sum_ +  d*2%9
        else:
            sum_ = sum_ + d

    # calculating final check sum
    check_sum = 10 - sum_%10

    return True if check_sum == check_number else False


class AgreeToTerms(forms.Form):
    """
    This form allows users who have not agreed yet
    to agree to terms
    """

    accept_terms_and_conditions = forms.BooleanField(required = True)
    accept_privacy_policy = forms.BooleanField(required = True)

    class Meta(UserCreationForm.Meta):
        model = User


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        super(AgreeToTerms, self).__init__(*args, **kwargs)

    @transaction.atomic
    def save(self):
        self.user.accepted_tcs = self.cleaned_data.get('accept_terms_and_conditions')
        self.user.accepted_privacy = self.cleaned_data.get('accept_privacy_policy')
        self.user.save(update_fields=['accepted_tcs', 'accepted_privacy'])
        return self.user


class MiiOwnerSignUpForm(UserCreationForm):
    """
    This sign up form allows MiiOwners to register on the site
    and will ascociate the user as a MiiOwner.
    """
    #remove comments to make sign up page less wordy
    # def __init__(self, *args, **kwargs):
    #     super(MiiOwnerSignUpForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #
    #     for fieldname in ['username', 'password1', 'password2']:
    #         self.fields[fieldname].help_text = None


    email = forms.EmailField(required = True)
    name = forms.CharField(required = True)
    surname = forms.CharField(required = True)
    accept_terms_and_conditions = forms.BooleanField(required = True)
    accept_privacy_policy = forms.BooleanField(required = True)

    class Meta(UserCreationForm.Meta):
        model = User

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_owner = True
        user.first_name = self.cleaned_data.get('name')
        user.last_name = self.cleaned_data.get('surname')
        user.email = self.cleaned_data.get('email')
        user.accepted_tcs = self.cleaned_data.get('accept_terms_and_conditions')
        user.accepted_privacy = self.cleaned_data.get('accept_privacy_policy')
        user.save()
        miiowner = MiiOwner.objects.create(user=user)
        return user


class MiiSitterSignUpForm(UserCreationForm):
    """
    This sign up form allows MiiOwners to register on the site
    and will ascociate the user as a MiiOwner.
    """
    #remove comments to make sign up page less wordy
    # def __init__(self, *args, **kwargs):
    #     super(MiiSitterSignUpForm, self).__init__(*args, **kwargs)
    #     self.helper = FormHelper()
    #
    #     for fieldname in ['username', 'password1', 'password2']:
    #             self.fields[fieldname].help_text = None


    email = forms.EmailField(required = True)
    name = forms.CharField(required = True)
    surname = forms.CharField(required = True)
    accept_terms_and_conditions = forms.BooleanField(required = True)
    accept_privacy_policy = forms.BooleanField(required = True)

    class Meta(UserCreationForm.Meta):
        model = User


    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email


    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_sitter = True
        user.first_name = self.cleaned_data.get('name')
        user.last_name = self.cleaned_data.get('surname')
        user.email = self.cleaned_data.get('email')
        user.accepted_tcs = self.cleaned_data.get('accept_terms_and_conditions')
        user.accepted_privacy = self.cleaned_data.get('accept_privacy_policy')
        user.save()
        miisitter = MiiSitter.objects.create(user=user)
        miisitter.save()
        return user


class ContactForm(forms.Form):
    """
    Form to be used when contacting MiiPets in the Contact page
    """
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
