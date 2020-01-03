from django.contrib import admin
from .models import Metrics, User, MiiOwner, Pets, MiiSitter
from .models import SitterServices ,SitterBooking

@admin.register(Metrics, User, MiiOwner, Pets, MiiSitter)
class UsersAdmin(admin.ModelAdmin):
    pass

@admin.register(SitterServices ,SitterBooking)
class ServicesAdmin(admin.ModelAdmin):
    pass
