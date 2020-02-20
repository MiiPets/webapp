from django.contrib import admin
from .models import Metrics, User, MiiOwner, Pets, MiiSitter, ServiceReviews, PayFastOrder
from .models import SitterServices ,ServiceBooking, ServicePhotos, ServiceLocation


@admin.register(SitterServices ,ServiceBooking,
                User, Metrics, MiiOwner, Pets,
                MiiSitter, ServiceReviews, ServicePhotos,
                ServiceLocation, PayFastOrder)
class ServicesAdmin(admin.ModelAdmin):
    pass
