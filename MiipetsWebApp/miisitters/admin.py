from django.contrib import admin
from .models import MiiSitter, SitterServices


@admin.register(MiiSitter)
class MiiSitterAdmin(admin.ModelAdmin):
    pass

@admin.register(SitterServices)
class SitterServicesAdmin(admin.ModelAdmin):
    pass
