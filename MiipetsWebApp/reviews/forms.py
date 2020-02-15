from django import forms
from django.db import transaction
from core.models import  User, SitterServices, ServiceReviews
from crispy_forms.helper import FormHelper
from better_profanity import profanity

class ReviewService(forms.ModelForm):

    class Meta():
        model = ServiceReviews
        fields = ['service', 'review_score', 'review_text', 'reviewer']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user',None)
        self.service = kwargs.pop('service', None)
        super(ReviewService, self).__init__(*args, **kwargs)
        # no reason to see the below field but it must be updated
        self.fields['reviewer'] = forms.ChoiceField(widget = forms.HiddenInput())


    @transaction.atomic
    def save(self):
        review = super().save(commit=False)

        # removing bad words
        review_text =  profanity.censor(self.cleaned_data.get('review_text'))

        review.reviewer = self.user
        review.service = self.service
        review.review_score = self.cleaned_data.get('review_score')
        review.review_text = review_text
        review.save()

        return review
