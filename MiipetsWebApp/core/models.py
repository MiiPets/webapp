from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from djmoney.models.fields import MoneyField
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

def image_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'profile_pictures/user_{}/{}'.format(instance.id, filename)


def image_directory_path_pet(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'pet_profile_pictures/pet_{}/owner_{}/{}'.format(instance.name,
                                                            instance.owner,
                                                            filename)


def image_directory_path_service_photos(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'service_pictures/service_{}/sitter_{}/{}'.format(instance.service.service_name,
                                                             instance.service.sitter.id,
                                                             filename)

def image_directory_path_service(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'service_pictures/service_{}/sitter_{}/{}'.format(instance.service_name,
                                                             instance.sitter.id,
                                                             filename)

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


class User(AbstractUser, TimeStampMixin):

    """
    Data that is required for all of the user types are defined in here
    with specific data in the lower tables.
    """

    # used to differentiate users
    is_owner = models.BooleanField(default=False)
    is_sitter = models.BooleanField(default=False)
    email = models.EmailField(max_length=254)
    profile_picture = ProcessedImageField(upload_to=image_directory_path,
                                          processors=[ResizeToFill(400, 400)],
                                          format='JPEG',
                                          options={'quality': 60})
    bio = models.TextField()
    accepted_tcs = models.BooleanField(default=False)
    accepted_privacy = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['email']
    def __str__(self):
        return ("User: {}, ID:{}".format(self.first_name, self.id))


class MiiOwner(TimeStampMixin):
    """
    This model class will store all the data related to the owners
    of pets and these users will then be able to book services on the
    app
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return ("MiiOwner: {}, ID: {}".format(self.user.first_name, self.user.id))


class Pets(TimeStampMixin):
    """
    This model class will store all the data related to the pets
    of owners. These pets will be visible to the providers/sitters
    when they receive a booking to give the provider/sitter as much
    detail as they can.
    """

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    breed = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    profile_picture = ProcessedImageField(upload_to=image_directory_path_pet,
                                          processors=[ResizeToFill(400, 400)],
                                          format='JPEG',
                                          options={'quality': 60})

    def __str__(self):
        return ("{} of MiiOwner: {}".format( self.name, self.owner.id))


class MiiSitter(TimeStampMixin):
    """
    This model class will store all the data related to the sitters.
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    merchant_id = models.CharField(max_length=40, default="")
    id_number = models.CharField(max_length=13, default="")
    validated = models.BooleanField(default=False)
    review_score = models.FloatField(default=6.0)
    number_of_bookings = models.PositiveIntegerField(default=0)

    def __str__(self):
        return ("MiiSitter ({}), ID: {}".format(self.user.first_name, self.user.id))


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

    SERVICE_CHOICES = [(WALK, 'Walker'),
                       (BOARD, 'Boarding'),
                       (SIT, 'House Sitting'),
                       (DAYCARE, 'Daycare')]

    allowed_to_show = models.BooleanField(default = False) # we first need to approve it
    review_score = models.FloatField(default = 6, validators=[MinValueValidator(0), MaxValueValidator(5)])
    number_of_reviews = models.PositiveIntegerField(default=0)
    sitter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service_name = models.CharField(max_length=50)
    type = models.CharField(max_length=50, choices=SERVICE_CHOICES, default=DAYCARE)
    dogs_allowed = models.BooleanField(default=False)
    cats_allowed = models.BooleanField(default=False)
    birds_allowed = models.BooleanField(default=False)
    reptiles_allowed = models.BooleanField(default=False)
    other_pets_allowed = models.BooleanField(default=False)
    description = models.TextField(null = "No description")
    price = models.PositiveIntegerField(default=10, validators=[MinValueValidator(10)])
    profile_picture = ProcessedImageField(upload_to=image_directory_path_service,
                                          processors=[ResizeToFill(400, 400)],
                                          format='JPEG',
                                          options={'quality': 100})
    maximum_number_of_pets = models.PositiveIntegerField(default=5, validators=[MaxValueValidator(12)])
    date_start = models.DateField()
    date_end = models.DateField()

    time_start_monday = models.PositiveIntegerField()
    time_start_tuesday = models.PositiveIntegerField()
    time_start_wednesday = models.PositiveIntegerField()
    time_start_thursday = models.PositiveIntegerField()
    time_start_friday = models.PositiveIntegerField()
    time_start_saturday = models.PositiveIntegerField()
    time_start_sunday = models.PositiveIntegerField()
    time_end_monday = models.PositiveIntegerField()
    time_end_tuesday = models.PositiveIntegerField()
    time_end_wednesday = models.PositiveIntegerField()
    time_end_thursday = models.PositiveIntegerField()
    time_end_friday = models.PositiveIntegerField()
    time_end_saturday = models.PositiveIntegerField()
    time_end_sunday = models.PositiveIntegerField()


    REQUIRED_FIELDS = ['service_name', 'type', 'price', 'pet_type']


    class Meta:
        order_with_respect_to = 'created_at'


    def __str__(self):
        return ("{} service, with sitter: {}".format(self.type,
                                                     self.sitter.id))


class ServicePhotos(TimeStampMixin):
    """
    This model class will store all the data related to the bookings
    related to sitters.
    """

    service = models.ForeignKey(SitterServices, on_delete=models.CASCADE)
    profile_picture = ProcessedImageField(upload_to=image_directory_path_service_photos,
                                          processors=[ResizeToFill(800, 800)],
                                          format='JPEG',
                                          options={'quality': 200})

    def __str__(self):
        return ("Photos of service {}".format(self.service))


class ServiceBooking(TimeStampMixin):
    """
    This model class will store all the data related to the bookings
    related to sitters.
    """

    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service = models.ForeignKey(SitterServices, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    time_slot = models.PositiveIntegerField()
    notified_sitter = models.BooleanField(default=False)
    sitter_answer = models.BooleanField(default = False)
    notified_owner_of_sitter_response = models.BooleanField(default=False)
    sitter_confirmed = models.BooleanField(default=False)
    owner_payed = models.BooleanField(default=False)
    invoice_sent = models.BooleanField(default=False)
    price = models.PositiveIntegerField(default=10, validators=[MinValueValidator(10)])
    price_in_cents = models.PositiveIntegerField(default=10, validators=[MinValueValidator(10)])
    number_of_pets = models.PositiveIntegerField(default=1)
    reason_for_not_being_able = models.CharField(default = "", max_length=500)

    def __str__(self):
        return ("Booking of service {} for user {}".format(self.service, self.requester))


class ServiceLocation(TimeStampMixin):
    """
    The location of the services will be stored here in
    streed adress that is converted to long lat
    """

    service = models.ForeignKey(SitterServices, on_delete=models.CASCADE)
    city = models.CharField(max_length=500)
    province = models.CharField(max_length=500)
    street_name = models.CharField(max_length=500, default="")
    area_code = models.PositiveIntegerField()
    street_number = models.CharField(max_length=500, default="")
    lattitude = models.FloatField()
    longitude = models.FloatField()

    class Meta:
        order_with_respect_to = 'created_at'


    def __str__(self):
        return ("Location of service {}".format(self.service.id))


class ServiceReviews(TimeStampMixin):
    """
    The location of the services will be stored here in
    streed adress that is converted to long lat
    """

    service = models.ForeignKey(SitterServices, on_delete=models.CASCADE)
    review_score = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    review_text = models.CharField(max_length=10000)
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return ("Review of service {}".format(self.service.id))


class PayFastOrder(TimeStampMixin):

    """
    Storing data of payfast payments
    """

    m_payment_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    pf_payment_id = models.CharField(max_length=40, unique=True, null=True, blank=True)
    payment_status = models.CharField(max_length=20, null=True, blank=True)
    item_name = models.CharField(max_length=100)
    item_description = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)


    custom_str1 = models.CharField(max_length=255, null=True, blank=True)
    custom_str2 = models.CharField(max_length=255, null=True, blank=True)
    custom_str3 = models.CharField(max_length=255, null=True, blank=True)
    custom_str4 = models.CharField(max_length=255, null=True, blank=True)
    custom_str5 = models.CharField(max_length=255, null=True, blank=True)

    custom_int1 = models.IntegerField(null=True, blank=True)
    custom_int2 = models.IntegerField(null=True, blank=True)
    custom_int3 = models.IntegerField(null=True, blank=True)
    custom_int4 = models.IntegerField(null=True, blank=True)
    custom_int5 = models.IntegerField(null=True, blank=True)

    #payer information
    name_first = models.CharField(max_length=100, null=True, blank=True)
    name_last = models.CharField(max_length=100, null=True, blank=True)
    email_address = models.CharField(max_length=100, null=True, blank=True)

    #Receiver Information
    merchant_id = models.CharField(max_length=15)
    merchant_key = models.CharField(max_length=40)
    sitter_merchant_id = models.CharField(max_length=15)
    sitter_percantage = models.FloatField(default = 0.2)
    user_pay = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    booking = models.ForeignKey(ServiceBooking, on_delete=models.CASCADE)
    # split info
    setup = models.CharField(max_length=200)
    # Security Information
    signature = models.CharField(max_length=32, null=True, blank=True)
    request_ip = models.GenericIPAddressField(null=True, blank=True)


    class HelpText:
        m_payment_id = "Unique transaction ID on the receiver's system."
        pf_payment_id = "Unique transaction ID on PayFast."
        payment_status = "The status of the payment."
        item_name = "The name of the item being charged for."
        item_description = "The description of the item being charged for."
        amount_gross = "The total amount which the payer paid."
        amount_fee = "The total in fees which was deducted from the amount."
        amount_net = "The net amount credited to the receiver's account."

        first_name_payer = "First name of the payer."
        last_name_payer = "Last name of the payer."
        email_address = "Email address of the payer."

        merchant_id = "The Merchant ID as given by the PayFast system."
        sitter_merchant_id = "The Merchant ID of sitter as given by the PayFast system."
        signature = "A security signature of the transmitted data"

    def __str__(self):
        return 'PayFastOrder {id} of booking'.format(self.m_payment_id, self.booking.id)

    class Meta:
        verbose_name = 'PayFast order'
