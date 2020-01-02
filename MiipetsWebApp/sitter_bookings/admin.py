from django.contrib import admin
from .models import SitterBooking

@admin.register(SitterBooking)
class SitterBookingAdmin(admin.ModelAdmin):
    pass
