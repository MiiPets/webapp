from django.contrib import admin
from .models import MiiOwner, Pets

@admin.register(MiiOwner)
class MiiOwnerAdmin(admin.ModelAdmin):
    pass

@admin.register(Pets)
class PetsAdmin(admin.ModelAdmin):
    pass
