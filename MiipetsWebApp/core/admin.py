from django.contrib import admin
from .models import Metrics

@admin.register(Metrics)
class MetricsAdmin(admin.ModelAdmin):
    pass
