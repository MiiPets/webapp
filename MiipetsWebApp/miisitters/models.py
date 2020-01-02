from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from core.models import image_directory_path, TimeStampMixin


class MiiSitter(TimeStampMixin):
    """
    This model class will store all the data related to the sitters.
    """

    name =  models.CharField(max_length=50)
    surname =  models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    contact_number = PhoneNumberField()
    profile_picture = models.ImageField(upload_to=image_directory_path)
    #location = AddressField()
    bio = models.TextField()

    def __str__(self):
        return ("MiiSitter with name: {} and surname: {}".format(self.name, self.surname))


class SitterServices(TimeStampMixin):
    """
    This model class will store all the data related to the pets
    of owners. These pets will be visible to the providers/sitters
    when they receive a booking to give the provider/sitter as much
    detail as they can.
    """

    WALK = 'WALK'
    BOARD = 'BOARD'
    SIT = 'SIT'
    DAYCARE = 'DAYCARE'
    FEED = 'FEED'

    SERVICE_CHOICES = [(WALK, 'Walker'),
                       (BOARD, 'Boarding'),
                       (SIT, 'House Sitting'),
                       (DAYCARE, 'Daycare'),
                       (FEED, 'Feeder')]

    sitter = models.ForeignKey(MiiSitter, on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=SERVICE_CHOICES, default=DAYCARE)
    description = models.TextField()
    price = models.FloatField()
    score = models.FloatField()

    def __str__(self):
        return ("Sitter activity of {} with sitter: {}, with pet name being {}".format(self.type, self.sitter))
