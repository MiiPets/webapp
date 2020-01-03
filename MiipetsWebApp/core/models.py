from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
#from address.models import AddressField

def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class TimeStampMixin(models.Model):

    """
    This model will be used to create fields for storing when a
    field is added to the database and when there was an update
    made to the field.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Metrics(TimeStampMixin):

    """
    This model will be used to create fields for storing when a
    field is added to the database and when there was an update
    made to the field.
    """

    total_owners = models.PositiveIntegerField()
    total_sitters = models.PositiveIntegerField()
    total_providers = models.PositiveIntegerField()
    total_pets = models.PositiveIntegerField()

    class Meta:
        ordering = ('-created_at',)


class User(AbstractUser):
    is_owner = models.BooleanField(default=False)
    is_sitter = models.BooleanField(default=False)


class MiiOwner(TimeStampMixin):
    """
    This model class will store all the data related to the owners
    of pets and these users will then be able to book services on the
    app
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name =  models.CharField(max_length=50)
    surname =  models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    # profile_picture = models.ImageField(upload_to=image_directory_path)
    #location = AddressField()

    def __str__(self):
        return ("MiiOwner with name: {} and surname: {}".format(self.name, self.surname))


class Pets(TimeStampMixin):
    """
    This model class will store all the data related to the pets
    of owners. These pets will be visible to the providers/sitters
    when they receive a booking to give the provider/sitter as much
    detail as they can.
    """

    owner = models.ForeignKey(MiiOwner, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    breed = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    profile_picture_path = models.ImageField(upload_to=image_directory_path)

    def __str__(self):
        return ("Pet of user: {}, with pet name being {}".format(self.owner, self.name))


class MiiSitter(TimeStampMixin):
    """
    This model class will store all the data related to the sitters.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
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
