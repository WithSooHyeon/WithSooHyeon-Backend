from django.contrib import admin
from .models import Counsel

# Register your models here.
@admin.register(Counsel)
class TodayModelAdmin(admin.ModelAdmin):
    pass