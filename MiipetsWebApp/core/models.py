from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
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
