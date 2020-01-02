from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from core.models import image_directory_path, TimeStampMixin
from miisitters.models import SitterServices
from miiowners.models import MiiOwner

class SitterBooking(TimeStampMixin):
    """
    This model class will store all the data related to the bookings
    related to sitters.
    """

    owner = models.ForeignKey(MiiOwner, on_delete=models.CASCADE)
    listing = models.ForeignKey(SitterServices, on_delete=models.CASCADE)
    date_start = models.DateField()
    date_end = models.DateField()
    approved =  models.BooleanField(default=False)


    def __str__(self):
        return ("Booking of {} activity on for owner {}".format(self.activity, self.date_start, self.owner))
