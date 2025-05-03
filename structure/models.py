from django.db import models


# Create your models here.

class StaticData(models.Model):
    kind = models.CharField(max_length=100, unique=True)
    place = models.CharField(max_length=100)
    name_ar = models.TextField(null=True, blank=True)
    name_en = models.TextField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    description_en = models.TextField(null=True, blank=True)
    description_ar = models.TextField(null=True, blank=True)
    info_en = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.kind


class ServicesModel(models.Model):
    static_data = models.ForeignKey(StaticData, on_delete=models.CASCADE, related_name="services")
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    description_ar = models.TextField(null=True, blank=True)
    description_en = models.TextField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)


class H_Vac_CategoryModel(models.Model):
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    description_ar = models.TextField(null=True, blank=True)
    description_en = models.TextField(null=True, blank=True)
    info_en = models.TextField(null=True, blank=True)
