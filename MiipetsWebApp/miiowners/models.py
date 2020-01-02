from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from core.models import image_directory_path, TimeStampMixin

class MiiOwner(TimeStampMixin):
    """
    This model class will store all the data related to the owners
    of pets and these users will then be able to book services on the
    app
    """

    name =  models.CharField(max_length=50)
    surname =  models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    profile_picture = models.ImageField(upload_to=image_directory_path)
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
