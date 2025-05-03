from django.contrib import admin
from .models import StaticData, ServicesModel
# Register your models here.


@admin.register(StaticData)
class StaticDataAdmin(admin.ModelAdmin):
    pass


@admin.register(ServicesModel)
class ServicesModelAdmin(admin.ModelAdmin):
    pass