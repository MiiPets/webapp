from django.contrib import admin
from .models import Metrics, User, MiiOwner, Pets, MiiSitter
from .models import SitterServices ,SitterBooking

@admin.register(SitterServices ,SitterBooking, User, Metrics, MiiOwner, Pets, MiiSitter)
class ServicesAdmin(admin.ModelAdmin):
    pass
