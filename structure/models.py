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
    images = models.TextField(null=True, blank=True)


class BannersModel(models.Model):
    url = models.URLField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)


class BlogsModel(models.Model):
    kind = models.CharField(max_length=100, default="news")
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    description_ar = models.TextField(null=True, blank=True)
    description_en = models.TextField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)


class OurClientsModel(models.Model):
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    location_ar = models.CharField(max_length=100)
    location_en = models.CharField(max_length=100)


class BrandsModel(models.Model):
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)


class CapacityModel(models.Model):
    start = models.CharField(max_length=100)
    end = models.CharField(max_length=100)


class ProductModel(models.Model):
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    description_ar = models.TextField(null=True, blank=True)
    description_en = models.TextField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    brand = models.ForeignKey(BrandsModel, on_delete=models.CASCADE, related_name="products")
    capacity = models.ForeignKey(CapacityModel, on_delete=models.CASCADE, related_name="products")
    specifications = models.TextField(null=True, blank=True)


class CategoryGeneratorSet(models.Model):
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)


class BrandGeneratorSetModel(models.Model):
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)


class ProductGeneratorSet(models.Model):
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    description_ar = models.TextField(null=True, blank=True)
    description_en = models.TextField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)
    category = models.ForeignKey(CategoryGeneratorSet, on_delete=models.CASCADE, related_name="products")
    brand = models.ForeignKey(BrandsModel, on_delete=models.CASCADE, related_name="products")


class FireProductsModel(models.Model):
    name_ar = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)
    description_ar = models.TextField(null=True, blank=True)
    description_en = models.TextField(null=True, blank=True)
    image = models.TextField(null=True, blank=True)



