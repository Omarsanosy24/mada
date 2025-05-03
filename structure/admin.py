from django.contrib import admin
from .models import StaticData
# Register your models here.


@admin.register(StaticData)
class StaticDataAdmin(admin.ModelAdmin):
    pass